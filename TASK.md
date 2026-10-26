# TASK.md — AgriSight milestone tracker
Updated 2026-10-26.

## M0 — Research foundation (IN PROGRESS)
- [x] Create private repository and core README, AGENTS.md, TASK.md, MEMORY.md.
- [x] Draft stakeholder decision questions, proposed criteria, initial source review and architecture ADRs.
- [x] M0-04: six-role synthetic KPI reconciliation with Python and SQLite, tests committed.
- [x] M0-05: compare framework documentation, create standard-library quality-contract fixture/tests, and audit NBS survey catalogue metadata.
- [ ] **M0-05 closure**: execute the same contract with Pandera AND GX Core in an environment with available dependencies; record results and choose a framework.
- [ ] Inspect actual survey questionnaires and variable codebooks, weights, geographic granularity and access permissions before ingestion.
- [ ] Approve person-role semantics, statuses, proper registration contract and realistic acceptance thresholds.
- [ ] Confirm M0-04/M0-05 complete GitHub CI runs and document commit-specific results.
- [ ] Finalize KPI dictionary and tested fixtures; address geographic privacy and boundary licensing.
- [ ] Obtain owner approval in docs/M0_REVIEW.md.

M0 is OPEN. No ingestion system, field enrollment, production database or dashboard yet.

## M1 — Seeded synthetic registry and approved data sources (PLANNED)
- [ ] Contract, seeded generator, known errors, source cards and benchmark.

## M2 — Database and analytics engineering (PLANNED)
- [ ] PostgreSQL model, dbt transformations, DuckDB reconciliation.

## M3 — Quality, identity and governance (PLANNED)
- [ ] Quality detection, reviewed duplicates, geographic/privacy tests.

## M4 — Data products (PLANNED)
- [ ] Power BI and Streamlit plus documented KPI agreement.

## M5 — Optional evidence-grounded AI (PLANNED)
- [ ] Read-only governance and evaluation go/no-go.

## M6 — Reproducibility and portfolio demonstration (PLANNED)
- [ ] CI, benchmarks, reports, sanitized release and owner approval.

**Immediate next:** run both frameworks in a network-enabled environment and assess survey variable dictionaries.
