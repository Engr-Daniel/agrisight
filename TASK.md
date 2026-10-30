# TASK.md — AgriSight roadmap

Updated: 2026-10-30. Checkboxes record observed evidence, not planned outputs.

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

## M2 — E2 agricultural findings and analytics engineering (COMPLETE: NASS-01 workflow)

Evidence and limits: [M2 technical review](docs/M2_REVIEW.md). Completion is the M1-approved first workflow, not all candidate questions or national inference.

- [x] Implement NASS-01 with source hash, unique/complete household keys, period guard, valid-response denominator and visible missing/invalid exclusions. Unweighted sample scope/no CI is explicit; RQ2 and population comparisons remain deferred.
- [x] Independently reconcile seven integer counts exactly and proportion/percentage at absolute tolerance 1e-12 in SQL/Python. Actual result 132859/143105 = 92.84022221445791%; 92.84% for display, pooled sample only.
- [x] Deliver [E2 findings](reports/E2_AGRICULTURAL_FINDINGS.md), versioned staging/eligibility/mart SQL, model/provenance documentation and tested commands. 52 tests and Ruff passed; installed wheel reproduces full JSON exactly. No new dependencies/services; PostgreSQL/dbt remain conditional.

## M3 - E3 robustness and separate engineering studies (COMPLETE: scoped experiments)

- [x] M3-01: pre-specify and execute the limited NASS-01 readiness audit; distinguish genuine sensitivity from target changes or software checks. No missing responses means no response-exclusion variation. [Protocol/shortlist](docs/experiments/E3_PROTOCOL.md), [assessment](reports/E3_READINESS.md).
- [x] M3-02: finalize [NASS-02 contract](docs/NASS02_INDICATOR_CONTRACT.md) after unit-label, plot-type and null checks. Measurement lineage remains unresolved; scope is explicitly the released field, not certified physical/GPS area. No companion-field backfill.
- [x] M3-03: execute same-target nonnegative missing-area bounds: 273887 plots, 48 missing areas, lower/upper median both6070.290058851242 in released labelled square metres. SQL/Python agree; 77 tests passed and installed wheel reproduces full JSON. [Findings](reports/E3_PLOT_AREA_BOUNDS.md), [empirical review](docs/M3_EMPIRICAL_REVIEW.md). Bounds are not population CIs or measurement-error bounds.
- [x] M3-04: implement labelled synthetic ground truth, fixed B0/B1 baselines and independent SQL accuracy checks. Development and reserved-seed runs executed; 104 tests pass and installed wheel reproduces full JSON. Mixed B1 duplicate recall50%, precision87.72-90.91%; no automatic merging. [Findings/review](reports/M3_SYNTHETIC_QUALITY.md), [protocol](docs/experiments/M3_04_PROTOCOL.md), [contract](docs/SYNTHETIC_REGISTRATION_CONTRACT.md).
- [x] M3-05: benchmark1000/10000/55000/100000 events with five timing and three separate traced-allocation repeats; independent correctness checks and installed-wheel55000-event smoke match. All123 tests pass. Collision guard rejects499500 potential pairs. [Protocol](docs/experiments/M3_05_PROTOCOL.md), [findings](reports/M3_WORKLOAD_BENCHMARK.md), [M3 review](docs/M3_REVIEW.md). Shared-machine batch scope, not total memory, SLA or agricultural findings.

## M4 - Evidence-backed reporting (COMPLETE: local read-only prototype)

- [x] M4-01: select Streamlit for one local read-only prototype and specify allowed metrics, source separation, valid selections, denominators, provenance/freshness and failure states. [ADR-004](docs/adr/ADR-004-initial-reporting-platform.md), [reporting contract](docs/M4_REPORTING_CONTRACT.md). No UI/dependency installation claimed.
- [x] M4-02: lock Streamlit 1.66.1 and 45 distributions while retaining all E1 pins; reproduce clean installation and packaged aggregate adapter/manifest. 45 new cases; 168 full tests pass in both M4 environments, Ruff/pip check pass. Actual bundles match except build UTC. [Schema](docs/M4_BUNDLE_SCHEMA.md), [review](docs/M4_ADAPTER_REVIEW.md). No dashboard or app-specific UI validation claimed.
- [x] M4-03: implement separate Streamlit views with 36 UI cases exercising all 126 quality cells, both survey indicators and 12 workload/measurement choices. All 204 tests pass in development/installed-wheel environments; actual aggregate headless displays and loopback startup/cleanup verified. [UI review](docs/M4_UI_REVIEW.md). Browser review followed in M4-04 below; no raw-data loading or experiment reruns.
- [x] M4-04: actual Chrome desktop/narrow rendering, keyboard navigation, source/limit visibility, charts/tables and provenance reviewed. Six browser checks passed across 19 captures; zero JavaScript exceptions and both temporary ports closed. All 204 tests pass in development/installed-wheel environments. [Combined review](docs/M4_REVIEW.md) records internal review scope and remaining coverage limits. Maps, geography/row-level drill-down and deployment remain gated and excluded.

- [x] M4-05: owner-requested agricultural visual refresh: packaged AI-generated landscape, responsive hero/navigation/cards/tables and preserved evidence context.212 installed-wheel tests pass; actual desktop/narrow Chrome review passes7 checks/19 captures, with cleanup regression coverage. [Visual review](docs/DASHBOARD_VISUAL_REVIEW.md), [asset/prompt record](docs/ILLUSTRATION_ASSETS.md). No metric/dependency/manifest change.

## M5 — Advanced analytics (OPTIONAL)

- [ ] Evaluate advanced statistics or evidence-grounded AI only for a justified need with baseline comparisons and appropriate tests.

## M6 — Publication and reproducibility (IN PROGRESS)

- [x] M6-01: clean committed-source audit in a new pinned environment; installed wheel, 204 tests, lint, deterministic synthetic run equality and missing-evidence failure behavior verified. [Protocol](docs/M6_REPRODUCTION_PROTOCOL.md), [review](docs/M6_REPRODUCTION_REVIEW.md). Full historical JSON differs in two line-ending-sensitive provenance hashes; exact reproduction is not complete.
- [x] M6-02: explicit LF text/raw-byte provenance policy; preserved historical inputs and manifest v1; regenerated synthetic evaluation and reviewed snapshot v2. Both autocrlf exports match, complete synthetic JSON and bundles reproduce, all 209 tests pass in development/installed-wheel environments. [Policy](docs/PROVENANCE_POLICY.md), [migration review](docs/M6_PROVENANCE_REVIEW.md). Survey/workload evidence remains historical.
- [x] M6-03: frozen authorized archive and committed-source wheel reproduce NASS-01/NASS-02 complete JSON and raw hashes exactly; all panels verified with unchanged manifest v2. Actual Ubuntu/Python3.11.17 GitHub CI:209 passed, lint/pip check success. [Protocol](docs/M6_SURVEY_REPRODUCTION_PROTOCOL.md), [review](docs/M6_SURVEY_REPRODUCTION_REVIEW.md). Benchmark limits retained; no new timing claim.
- [ ] M6-04: complete licence/privacy/disclosure/dependency/secrets and release-readiness review; explicit owner authorization before any new release or deployment. Existing GitHub repository is observed public; no visibility change is authorized or performed here.

**Immediate next:** M6-04: concrete release-readiness audit and remaining permission/disclosure/security decisions. Survey and synthetic reproduction plus actual remote fixture CI are verified; this does not authorize data redistribution or deployment. M5 remains optional.
