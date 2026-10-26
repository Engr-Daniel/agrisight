# TASK.md — AgriSight milestone tracker
Updated 2026-10-26.

## M0 — Research foundation (IN PROGRESS)
- [x] Private repository and README/AGENTS/TASK/MEMORY.
- [x] Stakeholder decision questions, preliminary source review and architecture ADRs.
- [x] M0-04 synthetic KPI reconciliations and automated tests.
- [x] M0-05 standard library validation contract and survey catalogue assessment.
- [x] Add optional experimental Pandera/GX script and manual GitHub Actions comparison workflow.
- [x] Run first comparison workflow and capture version/results (run 40355059389: successful; still partial semantic contract).
- [ ] Align both libraries to semantically equivalent missing-ID/strict-boolean validations and compare diagnostics.
- [ ] Inspect NASS/GHS survey codebooks, sampling variables, geography and actual file-level permissions.
- [ ] Confirm entity grain and acceptance criteria with owner; finalize KPI dictionary.
- [ ] Privacy threat-model and boundaries licence review.
- [ ] M0 review and explicit owner sign-off.

M0 NOT CLOSED. Do not claim Pandera/GX execution or data ingestion solely from committed prototypes.

## M1 — Seeded synthetic registry (PLANNED)
- [ ] Approved source cards, data model and generators.

## M2 — Relational/analytics models (PLANNED)
- [ ] PostgreSQL, dbt, DuckDB.

## M3 — Data quality/governance (PLANNED)
- [ ] Validation, duplicate evaluation, geographic/privacy.

## M4 — BI applications (PLANNED)
- [ ] Power BI, Streamlit dashboards.

## M5 — Optional AI analyst (PLANNED)
- [ ] Safety/evidence go/no-go.

## M6 — Final verification (PLANNED)
- [ ] CI, performance, documentation and release.

**Next:** trigger the manual M0 Validation Framework Comparison GitHub Action and examine results.
