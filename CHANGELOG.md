# Changelog

All notable changes to the earnings-analysis skill and its scoring engine are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.4.1] — Current

### Added
- **Whisper overrun regime branch.** Handles the "beat-maintain-negative reaction" pattern where a headline beat at low or medium stock elevation draws a negative reaction because narrow-band whisper expectations on a specific key metric were not met. Previously fell through to the "unknown" regime.
- **Capex-to-revenue ratio input** for the growth-capex-mode classifier. Companies with high capex intensity (>25% of revenue) are now classified as `GROWTH_CAPEX_MODE` regardless of revenue growth rate, capturing cases like Microsoft's $37.5B quarterly capex on 17% revenue growth.

### Changed
- **Growth capex mode threshold** lowered from 20% to 15% revenue growth as one of the qualifying conditions.

### Fixed
- `PROBLEMATIC_QUARTER` now correctly receives the `WITH_CRITICAL_FLAGS` suffix when critical flags are present, resolving a labelling inconsistency identified during the Novo Nordisk Q4 2025 test case.

## [1.4]

### Added
- **Year-over-year gross margin deterioration check.** Flags structural margin compression visible on an annual basis even when sequential change is not severe enough to trigger the existing margin pressure flag.
- **Regulatory overhang red flag category.** Adds `doj_investigation`, `sec_investigation`, `antitrust_review`, `regulatory_enforcement_action`, and `doj_settlement_risk` as distinct red flag keys with appropriate penalties.
- **Operating margin inputs.** Adds explicit operating margin change inputs (QoQ and YoY) to capture earnings quality dynamics in high-gross-margin businesses (pharma, software) where the real action is at the OPM level.
- **One-time beat direction split.** Separates `one_time_favourable` (beat flattered by non-recurring positive) from `one_time_unfavourable` (current period depressed by non-recurring negative). Retains legacy `one_time` mapping to `one_time_favourable` for backward compatibility.

## [1.3.1]

### Changed
- Base verdict is now computed from the composite score without critical flag gating.
- Critical flag downgrade modifier preserves the base verdict context in the verdict detail text, so the reader sees both the mechanical score and the specific concern that caused the downgrade.

## [1.3]

### Added
- **Core segment GM gap input.** Distinguishes cases where the consolidated gross margin understates core business quality.
- **Multi-period stock context** with the expectations elevation classifier (recent momentum, rally maturity, cushion erosion sub-scores).

## [1.2]

### Added
- **YoY trend suppression on QoQ margin noise.** Mix-quarter noise no longer fires the structural margin compression flag when the annual trend is positive.
- **Stock reaction overlay** with the expectations regime classifier. Introduces the constructive / overrun / depressed / balanced / deteriorating regimes.
- **GAAP/non-GAAP operating margin gap detection.** Flags large adjustment magnitudes that warrant investigation of whether excluded items are truly one-time.

## [1.1]

### Changed
- **OCF/NI is now the primary cash quality metric**, with FCF/NI demoted to secondary. OCF excludes capex variability, which makes it a cleaner read on earnings quality.
- **Guidance raise magnitude buckets** (modest, meaningful, massive) replace single-bucket guidance change handling.

## [1.0]

### Initial Release
- Three-layer scoring engine: beat quality, operational health, management signals.
- Five base verdict tiers: STRONG / SOLID / MIXED / WEAK / PROBLEMATIC.
- Initial flag library covering beat magnitude, gross margin trends, cash conversion, working capital discipline, governance red flags, and management tone.
- Four-layer analytical workflow: Parse → Compare → Diagnose → Decide.
- Sector-specific parsing checklist for ten sectors.
