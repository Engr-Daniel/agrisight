# TASK.md — AgriSight milestone tracker
Updated: 2026-10-26.

## M0 — Research foundation and architecture (IN PROGRESS)
- [x] Create private repository with README.md, AGENTS.md, TASK.md and MEMORY.md.
- [x] Draft ten stakeholder decision questions and actionable scenarios: `docs/M0_DECISION_QUESTIONS.md`.
- [x] Draft engineering acceptance tests and metrics: `docs/M0_ACCEPTANCE_CRITERIA.md`.
- [x] Review public metadata for two official Nigerian agricultural data sources: `docs/M0_SOURCE_ASSESSMENT.md`.
- [x] Draft initial stack/grain and geography/privacy ADRs: `docs/adr/`.
- [ ] Inspect source microdata codebooks, actual file access terms, sample variables, design variables, and geography.
- [ ] Confirm person-role counts, accepted status logic, synthetic distributions and performance targets through fixtures.
- [ ] Finalize KPI dictionary with tested numerator/denominator examples.
- [ ] Compare primary validation framework Pandera vs GX Core in a working proof of concept.
- [ ] Establish and **observe** passing local smoke tests, lint and GitHub Actions; record run URLs.
- [ ] Review privacy threat model, boundary licences and disclosure policy.
- [ ] Record owner M0 approval in `docs/M0_REVIEW.md`; only then move to M1.

**M0 status: design draft delivered; NOT closed.** Next: inspect actual datasets and design a first KPI fixture.

## M1 — Source acquisition and synthetic registry (PLANNED)
- [ ] Inventory approved survey downloads and data cards; verify rights and weights.
- [ ] Version synthetic registration form, entities and generators.
- [ ] Seed known overlaps, missingness, duplicate truth, geospatial anomaly labels.
- [ ] Test totals, constraints and repeatability.

## M2 — Analytics engineering (PLANNED)
- [ ] PostgreSQL schema/migrations, raw and curated paths.
- [ ] dbt staging/intermediate/marts, SQL contracts and documentation.
- [ ] Independent DuckDB/Python reconciliation.

## M3 — Data quality and governance (PLANNED)
- [ ] Validation, duplicate candidate review, injection benchmark and quality metrics.
- [ ] Auditable corrections, privacy/geometry validation and disclosure tests.

## M4 — Dashboard and geospatial evidence (PLANNED)
- [ ] Power BI management report and consistent DAX measures.
- [ ] Streamlit/Plotly exploratory and quality dashboard with protected maps.
- [ ] Reconcile displayed measures with canonical SQL output.

## M5 — Optional grounded natural-language analyst (GO/NO-GO)
- [ ] Evaluate necessity vs BI baseline.
- [ ] Read-only SQL safety design and benchmark for faithfulness, abstention, privacy.

## M6 — Release and portfolio proof (PLANNED)
- [ ] Full CI, clean environment, measured ingestion and query benchmark.
- [ ] Documented limitation-aware demonstration and owner-approved publication review.

## Next actionable assignment
**M0-04:** Obtain codebooks and source terms (without committing restricted files), define three priority KPI fixtures, and run them in both Python and SQL.
