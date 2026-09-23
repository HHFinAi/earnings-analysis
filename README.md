# Earnings analysis

A four-stage post-print research workflow: Parse → Compare → Diagnose → Decide.
Version: see [VERSION](VERSION). Maintained original: `HHFinAi/earnings-analysis`.

## Start here

Clone or download this repository. Install the **entire** `earnings-analysis`
folder in a host that supports Agent Skills, preserving `SKILL.md`, `scripts/`,
`references/` and `VERSION`. A ZIP should contain `earnings-analysis/SKILL.md`
and its sibling folders, not an extra wrapping directory. Other hosts can use
the Markdown as an instruction framework, but executing scripts and loading
references require separately available runtime capabilities. Native installation
and UI paths vary by product; do not assume identical support across platforms.

Ask: "Review this earnings release and transcript. I have not supplied consensus;
show the reported results and guidance, but do not invent beat/miss comparisons."

## Scorer v2 migration

Run `python scripts/score_earnings.py --input examples/incomplete.json`.
This example intentionally exits 2 with `INSUFFICIENT_DATA`, demonstrating the
absence of fabricated defaults. Run `--help` for individual metric arguments.

Inputs contain `ticker`, `quarter`, `metrics`, and optional `sources`/`as_of`.
Metrics can be raw explicit values or observation cells with `status`, `value`,
`source_id`, `reason` and `as_of`. Unknown and inapplicable values are not zeros.

The old scoring rules remain in `scripts/legacy_earnings.py`; only the v2 entry
point is supported. A full composite requires all consumed fields to be observed.
Pre-revenue companies, negative-EPS denominators, missing transcripts and other
inapplicable dimensions may need qualitative analysis instead of this rubric.

All thresholds and regime interpretations are **heuristics**, not calibrated
predictors of returns. Coverage is not confidence. This release has deterministic
input tests, not an empirical investment-performance benchmark. See
[validation notes](VALIDATION.md).

## Tests and distributions

`python -m unittest discover -s tests -v`

`VERSION` is the release authority. Equity bundles pin this component and should
refresh it through their upstream synchronization process, not edit their copies.
Historical usage instructions are retained under `docs/archive/` for provenance,
but the v2 contract in `SKILL.md` takes precedence.

## License

MIT; see [LICENSE](LICENSE). This is a research framework, not investment advice.
