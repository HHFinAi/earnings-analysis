# Validation scope — 2026-09-23

Deterministic tests cover missingness, observed zero, inapplicability, numeric and
category validation, duplicate flags, EPS denominator policy, source IDs and
complete-input dispatch. The real historical engine smoke test runs when its
preserved file is available. A missing historical file must fail packaging checks.

No LLM-output benchmark, live vendor-feed validation or return-prediction
calibration has been completed by this change. Do not describe this release as
empirically validated or production-ready based only on unit tests.

Before a release, independently check synthetic outputs and repeat on dated
primary-source fixtures with a retained consensus snapshot. Record model/runtime,
prompt commit, data cutoff, grader and test results. Evaluate numerical accuracy,
citation entailment, missing-data handling and analytical coverage separately.
