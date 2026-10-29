# TASK.md — AgriSight roadmap

Updated: 2026-10-29. Checkboxes record observed evidence, not planned outputs.

## M0 — Engineering research foundation (COMPLETE)

- [x] Stakeholder decision hypotheses, architecture options and provenance/privacy rules.
- [x] Seven synthetic-registration KPI contracts and independent Python/SQL fixture tests.
- [x] Seven-case Pandera/GX comparison; historical CI: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776119
- [x] Pandera-first working decision for initial Python validation.

M0 is a design baseline, not empirical findings, completed user validation or production readiness. Preserve the [historical review](docs/M0_REVIEW.md); no need to reopen M0.

## Review alignment — targeted correction

- [x] Align current purpose, roadmap and architecture with empirical intelligence plus trustworthy delivery; record [rationale/trade-offs](docs/REVIEW_ALIGNMENT.md).
- [x] Record provisional RQ1–RQ3, E1/E2/E3 outputs and [source selection matrix](docs/RESEARCH_FEASIBILITY.md); GHS remains an alternative.
- [x] Verify raw-data Git protection and foundation environment checks; Python 3.11.9, 19 tests passed and Ruff passed locally. Commands and limitations in MEMORY.md.
- [x] Select/lock E1.1 Stata-reading dependencies and reproduce a fresh Python 3.11.9 install; full JSON outputs match, 33 tests and Ruff pass. Later methods require their own selection/verification. Existing CI extended, no new workflow.

## M1 — Source feasibility, acquisition and E1 (COMPLETE: scoped suitability baseline)

Evidence and restrictions: [M1 technical review](docs/M1_REVIEW.md). This closes first-workflow suitability, not every agricultural module or population-estimation readiness.

- [x] M1-01: inspect relevant NASS questionnaire/codebooks/methodology and all 21 released schemas; consider exact GHS service fields. Four relevant modules profiled at record level.
- [x] M1-02: finalize feasibility decisions; select NASS-01 observed-sample main-season crop participation. Access conditions recorded; RQ1 narrowed, RQ2/RQ3 deferred explicitly.
- [x] M1-03: acquire owner-authorized NBS archive in ignored storage; record observed acquisition date, hash, inventory and CRC. Exact upstream transaction time/mirror byte equality remain unknown, not fabricated; local input version is frozen by hash.
- [x] M1-04: document units/keys, null/skip semantics, reference periods and design availability. Main-season period supported; dry-season conflict excluded from comparisons. Missing usable variance design explicitly blocks population inference.
- [x] M1-05: execute E1.1/E1.2 schema/activity/main-dry plot/input checks. Independent Pandas/SQLite key/response counts agree exactly.
- [x] M1-06: review exclusions: 48 missing plot areas and 15409 missing quantities retained; no destructive cleaning. Sample diagnostics clearly distinguished from population estimates.
- [x] M1-07: deliver scripts, pinned environment, protocols, report and limitations. Full E1.2 output reproduced across working/fresh Python 3.11.9 environments; 37 tests and Ruff passed.

**Exit evidence:** [design/period review](docs/data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md), [indicator contract](docs/NASS_INDICATOR_CONTRACT.md), [findings](reports/E1_REAL_DATA_PROFILING.md) and [technical review](docs/M1_REVIEW.md). Technical review is not external user validation or public-release permission.

## M2 — E2 agricultural findings and analytics engineering (PLANNED)

- [ ] Compute selected RQ1/RQ2 indicators with documented population, eligibility, denominator, period, missingness, applicable weights and verified uncertainty methods.
- [ ] Independently reconcile results using SQL/Python, with tolerances for estimates; report supported geographic scope and sample counts.
- [ ] Deliver reproducible agricultural findings. Introduce PostgreSQL/dbt only when persistence/model complexity justifies them, with contracts and tests.

## M3 — E3 robustness and separate engineering studies (PLANNED)

- [ ] Pre-specify and evaluate reasonable missingness, eligibility and definition alternatives for RQ3; report stability and limitations without causal claims.
- [ ] Separately implement labelled synthetic ground truth for defect/duplicate precision, recall and false positives.
- [ ] Benchmark documented workload sizes, including 55k role entries, with hardware/repeats and observed results. Never present simulated counts as agricultural findings.

## M4 — Evidence-backed reporting (PLANNED)

- [ ] Choose Power BI or Streamlit initially; build interactive reporting from checked findings. Add the second only for a distinct purpose.
- [ ] Reconcile filters/denominators, expose provenance and uncertainty, and test licensed geography/disclosure safeguards before maps or drill-down.

## M5 — Advanced analytics (OPTIONAL)

- [ ] Evaluate advanced statistics or evidence-grounded AI only for a justified need with baseline comparisons and appropriate tests.

## M6 — Publication and reproducibility (PLANNED)

- [ ] Independent clean reproduction, existing CI checks, measured performance and learning documentation.
- [ ] Licence/privacy/disclosure review and explicit owner authorization before public release or deployment.

**Immediate next:** M2 implements NASS-01 and its reconciled analytical model. Population/domain inference, dry-season comparisons and area/quantity analyses remain gated as recorded in the M1 review. No automatic move to dashboards or additional infrastructure.
