#!/usr/bin/env python3
"""Strict input gate for the historical earnings methodology; not a return model.

Missing, not-applicable and observed zero are distinct. No composite is emitted
unless every input consumed by the historical scorer is explicitly observed.
The unchanged historical implementation lives in legacy_earnings.py.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
NUMERIC = (
    "revenue_beat_pct", "eps_beat_pct", "gross_margin_change_bps",
    "gross_margin_change_yoy_bps", "gross_margin_vs_5y_percentile",
    "core_segment_gm_gap_pp", "operating_margin_change_qoq_bps",
    "operating_margin_change_yoy_bps", "ocf_conversion", "fcf_conversion",
    "dso_change_days", "inventory_growth_pct", "revenue_growth_pct",
    "gaap_nongaap_op_margin_gap_pp", "capex_to_revenue_ratio",
    "stock_1y_return_pct", "stock_return_from_low_pct", "stock_drawdown_from_high_pct",
)
CHOICES = {
    "guidance_change": ("raised", "raised_narrowed", "maintained", "narrowed_lowered",
                        "lowered", "withdrawn", "initiated", "not_provided"),
    "guidance_raise_magnitude": ("modest", "meaningful", "massive"),
    "beat_driver": ("volume", "mix", "pricing", "one_time_favourable",
                    "one_time_unfavourable", "one_time", "fx", "unknown"),
    "management_tone": ("bullish", "confident", "neutral", "cautious", "defensive", "evasive"),
    "stock_reaction": ("positive", "flat", "negative"),
}
FIELDS = NUMERIC + tuple(CHOICES) + ("red_flags",)


def surprise(actual, consensus, minimum_denominator=0.01):
    """Use percentage surprise only with a positive, non-negligible denominator.

The floor is an analyst-selected convention in the same units as consensus.
Negative/near-zero EPS retains an absolute difference, not a scored percentage.
"""
    for value in (actual, consensus, minimum_denominator):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Surprise inputs must be finite numbers")
    if minimum_denominator < 0:
        raise ValueError("minimum_denominator must be non-negative")
    delta = actual - consensus
    if consensus <= minimum_denominator:
        return {"absolute_difference": delta, "percentage": None, "status": "not_applicable"}
    return {"absolute_difference": delta, "percentage": 100 * delta / consensus, "status": "observed"}


def validate(data):
    """Return normalized observations and explicit missingness; never impute."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    extra = set(data) - set(FIELDS)
    if extra:
        raise ValueError("Unknown metric(s): " + ", ".join(sorted(extra)))
    values, states, provenance_missing = {}, {}, []
    for key in FIELDS:
        cell = data.get(key)
        state, value, source = "observed", cell, None
        if isinstance(cell, dict):
            extra_cell = set(cell) - {"status", "value", "source_id", "reason", "as_of"}
            if extra_cell:
                raise ValueError(f"{key}: unknown cell fields {sorted(extra_cell)}")
            state = cell.get("status", "missing")
            value, source = cell.get("value"), cell.get("source_id")
            if state not in ("observed", "missing", "not_applicable"):
                raise ValueError(f"{key}: invalid observation status")
            if state != "observed":
                if value is not None:
                    raise ValueError(f"{key}: non-observed cells cannot carry a value")
                if state == "not_applicable" and not cell.get("reason"):
                    raise ValueError(f"{key}: not_applicable requires a reason")
        elif cell is None:
            state = "missing"
        if state == "observed":
            if key in NUMERIC:
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    raise ValueError(f"{key}: expected a finite number")
                if key in ("gross_margin_vs_5y_percentile", "stock_drawdown_from_high_pct") and not 0 <= value <= 100:
                    raise ValueError(f"{key}: expected 0 to 100")
                if key == "capex_to_revenue_ratio" and value < 0:
                    raise ValueError(f"{key}: expected non-negative percent of revenue")
            elif key in CHOICES:
                if value not in CHOICES[key]:
                    raise ValueError(f"{key}: unsupported category {value!r}")
            elif not isinstance(value, list) or any(not isinstance(v, str) for v in value):
                raise ValueError("red_flags must be a list of strings; [] means explicitly reviewed and none found")
            if key == "red_flags" and len(value) != len(set(value)):
                raise ValueError("Duplicate red_flags would double-count penalties")
            values[key] = value
            if not isinstance(source, str) or not source.strip():
                provenance_missing.append(key)
        if key == "beat_driver" and value == "unknown":
            state = "missing"
            values.pop(key, None)
        states[key] = state
    return values, states, provenance_missing


def _load_engine():
    path = Path(__file__).with_name("legacy_earnings.py")
    spec = importlib.util.spec_from_file_location("hhfinai_legacy_earnings", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(data, engine=None):
    values, states, provenance_missing = validate(data)
    missing = [k for k, v in states.items() if v == "missing"]
    na = [k for k, v in states.items() if v == "not_applicable"]
    # Magnitude is not consumed for these guidance states. This is not evidence
    # imputation: the historical function ignores the argument on these branches.
    ignored = []
    if values.get("guidance_change") not in (None, "raised", "lowered"):
        ignored = ["guidance_raise_magnitude"]
        missing = [k for k in missing if k not in ignored]
        na = [k for k in na if k not in ignored]
    required = [k for k in FIELDS if k not in ignored]
    result = {
        "version": VERSION,
        "status": "INSUFFICIENT_DATA" if missing else ("NOT_COMPARABLE" if na else "COMPLETE"),
        "composite": None,
        "data_quality": {
            "observed": sum(states[k] == "observed" for k in required),
            "required": len(required),
            "coverage": sum(states[k] == "observed" for k in required) / len(required),
            "missing": missing, "not_applicable": na, "ignored_fields": ignored,
            "missing_source_ids": [k for k in provenance_missing if k in required],
            "states": states,
        },
        "observations": data,
        "limitations": ["Methodology score, not a calibrated return forecast or success probability.",
                        "Complete input coverage does not establish factual accuracy or source quality.",
                        "Historical regime labels and narratives are hypotheses requiring independent evidence."],
    }
    if missing or na:
        return result
    e = engine or _load_engine()
    def args(names):
        return [values[k] for k in names.split()]
    elevation = e.classify_expectations_elevation(*args(
        "stock_1y_return_pct stock_return_from_low_pct stock_drawdown_from_high_pct"))
    beat_values = dict(values)
    if ignored:
        beat_values["guidance_raise_magnitude"] = "modest"  # ignored by historical function
    beat = e.score_beat_quality(*(beat_values[k] for k in (
        "revenue_beat_pct eps_beat_pct guidance_change guidance_raise_magnitude "
        "gross_margin_change_bps gross_margin_change_yoy_bps gross_margin_vs_5y_percentile "
        "core_segment_gm_gap_pp beat_driver operating_margin_change_qoq_bps "
        "operating_margin_change_yoy_bps").split()))
    ops = e.score_operational_health(*args(
        "ocf_conversion fcf_conversion dso_change_days inventory_growth_pct revenue_growth_pct "
        "gaap_nongaap_op_margin_gap_pp capex_to_revenue_ratio"))
    mgmt = e.score_management_signals(*args(
        "management_tone red_flags stock_reaction revenue_beat_pct eps_beat_pct guidance_change"), elevation["elevation"])
    result.update(composite=e.compute_composite(beat, ops, mgmt, elevation),
                  expectations_elevation=elevation, beat_quality=beat,
                  operational_health=ops, management_signals=mgmt)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON with ticker, quarter and metrics")
    parser.add_argument("--ticker")
    parser.add_argument("--quarter")
    for field in NUMERIC:
        parser.add_argument("--" + field.replace("_", "-"), type=float)
    for field, choices in CHOICES.items():
        parser.add_argument("--" + field.replace("_", "-"), choices=choices)
    parser.add_argument("--red-flags", help='JSON list; explicitly pass [] after review')
    ns = parser.parse_args()
    try:
        if ns.input:
            if ns.ticker or ns.quarter or any(getattr(ns, f) is not None for f in FIELDS):
                raise ValueError("Use --input OR individual arguments, not both")
            payload = json.loads(ns.input.read_text(encoding="utf-8"))
            if not isinstance(payload, dict) or set(payload) - {"ticker", "quarter", "metrics", "sources", "as_of"}:
                raise ValueError("Expected ticker, quarter, metrics and optional sources/as_of")
            ticker, quarter, metrics = payload.get("ticker"), payload.get("quarter"), payload.get("metrics", {})
        else:
            ticker, quarter = ns.ticker, ns.quarter
            metrics = {f: getattr(ns, f) for f in FIELDS if getattr(ns, f) is not None}
            if "red_flags" in metrics:
                metrics["red_flags"] = json.loads(metrics["red_flags"])
            payload = {}
        if not isinstance(ticker, str) or not ticker.strip() or not isinstance(quarter, str) or not quarter.strip():
            raise ValueError("ticker and quarter are required non-empty strings")
        result = assess(metrics)
        result.update(ticker=ticker, quarter=quarter)
        for key in ("sources", "as_of"):
            if key in payload:
                result[key] = payload[key]
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["status"] == "COMPLETE" else 2
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"version": VERSION, "status": "INVALID_INPUT", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
