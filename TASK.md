# TASK.md — AgriSight milestone tracker
Updated: 2026-10-26. **No implementation milestone has been completed.**

Legend: [ ] not done; [x] completed with linked evidence; [~] in progress (mark with plain text, not as checked).

## M0 — Charter, architecture, research foundations (IN PROGRESS)
- [x] Establish private repository and project documentation scaffold (initial commit; verify GitHub file tree).
- [x] Create AGENTS.md, TASK.md, MEMORY.md and initial docs (this initial scaffold commit).
- [ ] Confirm practical stakeholder personas and top ten decision questions; validate with realistic examples.
- [ ] Approve problem statement, scope exclusions, project hypotheses and measurable success criteria.
- [ ] Review permitted official datasets, licensing/access conditions, survey weighting, spatial precision and geographic representativeness.
- [ ] Finalize record grain, person-role relationships and synthetic population definition (55k *roles* vs *unique persons*).
- [ ] Choose Pandera **or** GX Core as primary validation library via a short ADR.
- [ ] Approve architecture ADRs covering PostgreSQL, dbt/adapter, DuckDB, PostGIS, Power BI and Streamlit responsibilities.
- [ ] Specify security and privacy threat model; initial data retention and public demo boundaries.
- [ ] Verify clean checkout, venv setup, smoke test and CI on an actual runner; capture versions and results.
- [ ] Owner signs off M0 decisions in `docs/M0_REVIEW.md` before M1.

**Exit evidence:** approved charter, decisions, source assessment, KPI dictionary, data governance strategy, repository baseline tests.

## M1 — Dataset and synthetic registry design (PLANNED)
- [ ] Create source inventory with official links, download date, permissions, survey metadata and limitations.
- [ ] Define farmer and women processor instruments and a versioned dictionary (synthetic demonstration).
- [ ] Implement reproducible seeded generators with person/role overlap, geography constraints and explicit distributions.
- [ ] Inject labelled defects (duplicates, missingness, invalid ranges, false coordinates, outliers).
- [ ] Prove record totals, referential integrity and deterministic re-runs with tests.
**Exit evidence:** source/data cards, generator specification, example schema, verified counts and tests.

## M2 — Modelling and transformations (PLANNED)
- [ ] Set up PostgreSQL and reproducible migrations; explicit indices and entity relationships.
- [ ] Create ingestion and immutable raw/curated layers.
- [ ] Introduce dbt staging, intermediate and marts models, tests and generated documentation.
- [ ] Create documented SQL metric definitions; independent DuckDB/Python reconciliation.
**Exit evidence:** tested ETL/dbt project, schema diagram, KPI documentation, reproducible SQL checks.

## M3 — Quality, identity and governance (PLANNED)
- [ ] Implement schema/range/consent/date/geography validation and operational quality scoring.
- [ ] Design duplicate-candidate matching + human-review protocol, not blind deletions.
- [ ] Evaluate precision, recall and false positives on known simulated truth.
- [ ] Validate geography, coordinate accuracy assumptions and privacy-preserving aggregation.
- [ ] Record quality incidents, corrections and audit trails.
**Exit evidence:** quality dashboard dataset, labelled evaluation set, error-analysis report, privacy tests.

## M4 — Decision support dashboards (PLANNED)
- [ ] Define design system and wireframes for management, operations and data-quality audiences.
- [ ] Implement Power BI model, DAX measures and reconciled KPI outputs.
- [ ] Build Streamlit multipage demonstrator with Plotly and approved aggregated maps.
- [ ] Test drill-downs, denominators, sorting, filtering and sensitive-data exposure.
**Exit evidence:** validated report files, app, screenshots marked synthetic/real, user test log.

## M5 — Optional grounded AI analyst (PLANNED / GO-NO-GO)
- [ ] Decide necessity after M4; compare with manual filtering and search.
- [ ] Build strictly read-only SQL generation/validation against curated views (if approved).
- [ ] Create benchmark questions including insufficient-data and privacy-refusal cases.
- [ ] Evaluate SQL validity, answer correctness, numerical faithfulness, abstention and latency.
**Exit evidence:** benchmark, error taxonomy, limitations and explicit go/no-go.

## M6 — Release engineering, demonstration and reporting (PLANNED)
- [ ] CI with test/lint checks, reproducible environment, dependency scans.
- [ ] Benchmark ingestion, transformation, refresh and dashboard response on stated hardware.
- [ ] Produce end-to-end report, architecture diagram, setup walkthrough and demo scenario.
- [ ] Prepare sanitized portfolio materials and verify licences and permissions.
- [ ] Obtain explicit owner authorization before publishing any code, data or deployment publicly.
**Exit evidence:** versioned release, benchmark artifacts, independently runnable instructions.

## Immediate next task
Conduct **M0-01: stakeholder questions and measurable success criteria**. Produce a reviewed list of decisions the dashboards must support before building any data generator.
