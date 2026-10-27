# TASK.md — AgriSight milestone tracker
Updated 2026-10-27.

## M0 — Research foundation (IN PROGRESS)
- [x] Private repository and README/AGENTS/TASK/MEMORY.
- [x] Stakeholder questions, source metadata review and architecture ADR drafts.
- [x] M0-04 role-level KPI reconciliation using Python/SQLite and tests.
- [x] M0-05 initial validation and first successful Pandera/GX Core comparison.
- [x] Add seven matched acceptance/rejection cases for framework comparison.
- [ ] Verify seven-case execution and document observed parity and versions.
- [ ] Compare error diagnostics, missing columns, nulls and typed data beyond pass/fail.
- [ ] Inspect NASS/GHS survey codebooks, sample weights, geography and file-level permissions.
- [ ] Agree role-vs-person grain, business status definitions and measurable acceptance thresholds.
- [ ] Finalize KPI dictionary with tested numerator/denominator fixtures.
- [ ] Complete privacy threat-model, geospatial boundary licence review.
- [ ] Record explicit owner M0 review and approval.

M0 remains OPEN. Do not treat proposed architecture or metadata audits as complete ingestion/fieldwork.

## M1 — Approved sources and seeded synthetic registry (PLANNED)
- [ ] Data cards, model, generator, injected defects and deterministic tests.
## M2 — Database and analytics engineering (PLANNED)
- [ ] PostgreSQL, dbt and DuckDB reconciliation.
## M3 — Quality/identity/governance (PLANNED)
- [ ] Validation, duplicate evaluation and privacy checks.
## M4 — Decision-support dashboards (PLANNED)
- [ ] Power BI, Streamlit and geographic analytics.
## M5 — Optional grounded analyst (PLANNED)
- [ ] Read-only SQL and evidence evaluation go/no-go.
## M6 — Release engineering (PLANNED)
- [ ] CI, benchmarks and owner-approved portfolio release.

**Next:** verify matched comparison run and inspect actual source dictionaries.
