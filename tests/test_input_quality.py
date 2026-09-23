import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scorer", ROOT / "scripts/score_earnings.py")
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


def complete():
    data = {name: 0.0 for name in scorer.NUMERIC}
    data.update(guidance_change="maintained", guidance_raise_magnitude="modest", beat_driver="volume",
                management_tone="neutral", stock_reaction="flat", red_flags=[])
    return data


class InputTests(unittest.TestCase):
    def test_empty_abstains(self):
        r = scorer.assess({})
        self.assertEqual(r["status"], "INSUFFICIENT_DATA")
        self.assertIsNone(r["composite"])
        self.assertEqual(r["data_quality"]["coverage"], 0)

    def test_observed_zero_is_not_missing(self):
        v, states, _ = scorer.validate({"revenue_beat_pct": 0})
        self.assertEqual(v["revenue_beat_pct"], 0)
        self.assertEqual(states["revenue_beat_pct"], "observed")
        self.assertEqual(states["ocf_conversion"], "missing")

    def test_not_applicable_is_not_zero(self):
        d = complete()
        d["eps_beat_pct"] = {"status": "not_applicable", "reason": "Negative consensus EPS"}
        r = scorer.assess(d)
        self.assertEqual(r["status"], "NOT_COMPARABLE")
        self.assertIsNone(r["composite"])

    def test_unknown_fields_fail(self):
        with self.assertRaises(ValueError):
            scorer.assess({"revenue_baet_pct": 5})

    def test_nonfinite_and_bool_fail(self):
        for v in (float("nan"), float("inf"), True):
            with self.subTest(value=v), self.assertRaises(ValueError):
                scorer.validate({"revenue_beat_pct": v})

    def test_invalid_category_fails(self):
        with self.assertRaises(ValueError):
            scorer.validate({"guidance_change": "maintaned"})

    def test_duplicate_flags_fail(self):
        with self.assertRaises(ValueError):
            scorer.validate({"red_flags": ["restatement", "restatement"]})

    def test_na_needs_reason_and_no_value(self):
        for cell in ({"status": "not_applicable"}, {"status": "missing", "value": 0}):
            with self.subTest(cell=cell), self.assertRaises(ValueError):
                scorer.validate({"eps_beat_pct": cell})

    def test_negative_eps_uses_absolute_difference(self):
        r = scorer.surprise(-0.20, -0.30)
        self.assertAlmostEqual(r["absolute_difference"], 0.10)
        self.assertIsNone(r["percentage"])

    def test_near_zero_eps_not_percent(self):
        self.assertIsNone(scorer.surprise(0.05, 0.001)["percentage"])
        self.assertAlmostEqual(scorer.surprise(1.10, 1.0)["percentage"], 10)

    def test_complete_dispatches_in_correct_order(self):
        engine = Mock()
        engine.classify_expectations_elevation.return_value = {"elevation": "low"}
        engine.compute_composite.return_value = {"composite_score": 0}
        r = scorer.assess(complete(), engine)
        self.assertEqual(r["status"], "COMPLETE")
        engine.score_beat_quality.assert_called_once_with(0., 0., "maintained", "modest", 0., 0., 0., 0., "volume", 0., 0.)
        self.assertEqual(r["data_quality"]["coverage"], 1)

    def test_unused_guidance_magnitude_not_required(self):
        d = complete()
        del d["guidance_raise_magnitude"]
        engine = Mock()
        engine.classify_expectations_elevation.return_value = {"elevation": "low"}
        self.assertEqual(scorer.assess(d, engine)["status"], "COMPLETE")
        d["guidance_change"] = "raised"
        self.assertEqual(scorer.assess(d)["status"], "INSUFFICIENT_DATA")

    def test_incomplete_does_not_call_engine(self):
        engine = Mock()
        scorer.assess({"revenue_beat_pct": 5}, engine)
        self.assertEqual(engine.mock_calls, [])

    def test_explicit_source_ids_preserved(self):
        d = {k: {"status": "observed", "value": v, "source_id": "S1"} for k, v in complete().items()}
        _, _, missing = scorer.validate(d)
        self.assertEqual(missing, [])

    @unittest.skipUnless((ROOT / "scripts/legacy_earnings.py").exists(), "Historical engine available in repository/CI")
    def test_real_engine_smoke(self):
        self.assertIsInstance(scorer.assess(complete())["composite"]["composite_score"], (int, float))


if __name__ == "__main__":
    unittest.main()
