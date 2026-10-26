# TASK.md — AgriSight milestones
Updated 2026-10-26.

## M0 — Research foundation (IN PROGRESS)
- [x] Private repository and starter documents.
- [x] Ten stakeholder decision questions and proposed actions.
- [x] Draft M0 evaluation framework and official survey metadata review.
- [x] Draft architecture and geography/privacy ADRs.
- [x] M0-04: implement synthetic six-role KPI fixture and independent Python/SQL calculations (9 focused tests passed in isolated local test environment; see lab).
- [ ] Review actual microdata codebooks, permissions, variable definitions and geography.
- [ ] Approve person-role interpretation, statuses and realistic validation rules.
- [ ] Finalize versioned KPI dictionary and expanded test fixtures.
- [ ] Compare Pandera vs GX Core in a practical example.
- [ ] Verify clean-clone dependency installation, full suite, Ruff and GitHub Actions run.
- [ ] Review geographic privacy policy, boundary licence and threat model.
- [ ] Owner sign-off in docs/M0_REVIEW.md.

**M0 remains OPEN.** Initial KPI fixture validates example definitions only.

## M1 — Approved sources and seeded 55k synthetic demonstration (PLANNED)
- [ ] source provenance; schema; generator with known defects and deterministic tests.

## M2 — Database and transformations (PLANNED)
- [ ] PostgreSQL relationships, migrations, dbt models, reconciliation.

## M3 — Quality, identity and governance (PLANNED)
- [ ] validation, supervised deduplication, injected-error evaluation, privacy.

## M4 — Visualizations (PLANNED)
- [ ] Power BI and Streamlit reporting with verified metric contracts and GIS.

## M5 — Optional grounded analyst (PLANNED)
- [ ] go/no-go, safe read-only queries and factual evaluation.

## M6 — Benchmarks, deployment and portfolio release (PLANNED)
- [ ] CI, performance, documentation and explicit owner publication approval.

**Next:** M0-05 source dictionary and quality-framework comparison, followed by complete environment testing.
