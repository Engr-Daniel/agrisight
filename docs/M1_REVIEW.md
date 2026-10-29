# M1 technical completion review — source suitability and E1

Date: 2026-10-29. **Technical disposition: M1 complete for the first-workflow suitability baseline, with binding M2 scope restrictions.** This is not a stakeholder signature, source-producer endorsement or approval for population inference/publication. M0 is not reopened.

## Definition of completion

M1 establishes whether the acquired source can support a first reproducible analysis and exposes its limitations. It need not make every provisional question answerable. The original investigation plan permits an explicit scope restriction when design information is missing. The concrete first workflow is now NASS-01: observed-sample main-season crop participation. Cross-season, quantity/area-based and population analyses are not silently considered ready.

| Task | Evidence / disposition |
|---|---|
| M1-01: source documentation and alternatives | NASS questionnaire, relevant codebooks, methodology sections and all 21 file schemas inspected; GHS extension-services exact fields considered. Detailed record-level work covers 4 modules, not all 21. See design/source reviews. |
| M1-02: feasibility and source selection | Source hash, access conditions and exact-variable matrix documented; NASS retained for first sample workflow; RQ1 narrowed, RQ2/RQ3 deferred with reasons. NASS-01 contract selected. |
| M1-03: local acquisition/provenance | Owner reports NBS download after signed-in application; local immutable copy hash/size/member inventory and CRC verified. Acquisition 2026-10-29 recorded. Exact upstream download time and independent mirror byte equality remain unknown, not invented. Observed application conditions govern local use. |
| M1-04: units/design/period/null contracts | Household/plot/input grains tested; main-season period supported. Dry-season conflict identified and excluded from time comparisons. Missingness/skip rules distinguished. Missing usable variance-design specification explicitly blocks population inference. |
| M1-05: executed E1 checks/reconciliation | Real household/main-plot/dry-plot/input profiling executed; schema inventory; activity/range/null/skip/duplicate/orphan checks. Key/response measures independently reconciled in Pandas and SQLite; synthetic tests check known truth. |
| M1-06: findings and exclusions | 48 missing plot areas; 15409 missing input quantities; no destructive correction. Appropriate restrictions recorded. Unweighted sample diagnostics not population estimates. |
| M1-07: reproducibility and report | Pinned E1 environment, protocols, executable modules, aggregate findings report, tests and clean-environment reproduction; final results recorded in MEMORY.md. |

## Review findings and engineering judgement

No selected-key duplicate excess, missing keys or orphan links were found; this does not prove all respondents are distinct humans or that answers are accurate. Valid infrastructure codes do not measure service access. The newly observed missing quantities and conflicting season references are retained as evidence, not suppressed.

The analyst may use only the [NASS-01 contract](NASS_INDICATOR_CONTRACT.md) as the initial M2 measure. No arbitrary data-quality score, threshold, imputation, blind deduplication, precision estimate or impact claim is introduced. GHS service variables establish an alternative's conceptual fit, not GHS empirical readiness.

## Carry-forward gates (do not disappear when M1 closes)

- Obtain verified household design/replicate information and weight applicability before any population CI, domain prevalence or significance claim; do not reconstruct design from geography labels alone.
- Resolve dry-season year conflict before cross-season analysis.
- Review quantity missingness/eligibility and area denominators before quantity totals, usage rates or yields.
- Complete source/licence/disclosure review and owner authorization before any public release; honour source citation and report-copy obligations. No publication or external message has occurred.
- Verify any new source/release independently; the current hash contract is not a producer certificate. No additional authenticated terms were independently observed beyond the supplied application snapshot and owner report.

## Evidence references

Verification observed: 37 tests passed; Ruff passed; full E1.2 aggregate JSON reproduced exactly across working/fresh Python 3.11.9 environments. E1.1 key/response counts reconcile in both main/dry-season runs. See MEMORY.md for commands and final file/link/privacy checks. No GitHub/Linux run is claimed.

- [Source/access card](data_sources/NASS_2023_CARD.md), [archive inventory](data_sources/NASS_2023_INVENTORY.md), [design/period review](data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md).
- [Feasibility matrix](RESEARCH_FEASIBILITY.md), [indicator contract](NASS_INDICATOR_CONTRACT.md).
- [Versioned input dictionary/contract](data_sources/NASS_CONTRACT_v1.md): keys, units, missingness, relationships, spatial/access assumptions.
- [E1.1 protocol](experiments/E1_PROTOCOL.md), [E1.2 protocol](experiments/E1_EXTENSION_PROTOCOL.md), [observed report](../reports/E1_REAL_DATA_PROFILING.md).
- [Pinned setup](DEVELOPMENT.md), existing test/CI definitions and actual verification log in MEMORY.md. GitHub/Linux results are not presumed from Windows execution.
