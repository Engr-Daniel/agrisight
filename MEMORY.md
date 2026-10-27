# MEMORY.md — AgriSight project memory
Updated 2026-10-27.

## Status
Private Engr-Daniel/agrisight, development on master. Owner: Oyewale Daniel. M0 **design baseline completed for synthetic-registry lane**; external survey and GIS use remain conditional on further due diligence. No real field registration, 55k synthetic dataset, dashboard, model deployment or proven outcomes exist.

## Design decisions
- Person is an opaque synthetic identity; one person may carry farmer and processor roles. Targets 50k/5k indicate synthetic **roles**, not guaranteed distinct persons.
- Status pending/accepted/rejected; completeness independent. Role vs unique-person KPIs explicitly separated.
- Canonical future metrics in SQL/dbt; PostgreSQL operational data, DuckDB/Python for independent checks; Power BI management output and Streamlit demonstrator.
- Pandera first for M1 Python validation; GX Core optional for later documented use, not a required ongoing workflow. Seven case agreement observed, not comprehensive performance/diagnostics parity.
- Separate synthetic registration records and licensed public survey samples. No client-specific data.
- No actual GPS, contact details, individual identities or fine-grained real survey locations; maps require licensed boundaries/privacy tests.
- Lightweight CI is sufficient, no unnecessary feature branches or orchestration.

## Evidence
- M0-04 six synthetic submissions, four accepted role entries, three distinct accepted persons, two accepted farmer roles and two processor roles; verified Python/SQL fixture.
- GitHub foundation CI passed: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776063
- Pandera 0.35 / GX 1.24.1 seven-scenario experiment passed: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776119 (tiny cases only).
- Source selection/limitations recorded in docs/M0_SOURCE_DECISION.md; official NASS/GHS codebooks, file licensing, weights and raw data NOT downloaded or inspected.
- Technical M0 completion review: docs/M0_REVIEW.md. User requested M0 completion; no signed itemized approval is represented.

## Next
M1-01 schema, grain, synthetic distributions, seeded defect scenarios, tests; official data lane gated pending actual files/docs/license/weight inspection.
