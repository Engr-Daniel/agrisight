# TASK.md — AgriSight milestone tracker
Updated: 2026-10-27.

## M0 — Foundation and engineering design (COMPLETE for synthetic registry track)
- [x] Project charter, stakeholder questions and decision workflows.
- [x] Draft architecture and role/person grain design.
- [x] KPI-01 to KPI-07 operational definitions with independent Python and SQLite fixtures.
- [x] Code-first quality baseline and seven matched Pandera/GX fixture outcomes.
- [x] Document CI evidence: Foundation CI 40495776063 and comparison 40495776119 successful.
- [x] Select Pandera as initial Python validation tool using ADR-003.
- [x] Source selection, survey design limitations and pre-ingestion licence gate.
- [x] Initial privacy threat model and geography prerequisites.
- [x] Publish technical M0 review and M1 entry conditions (`docs/M0_REVIEW.md`).

**Scope note:** these are design decisions and test fixtures, not approved field practices or deployed software. The owner may revisit assumptions; formal line-by-line owner ratification remains unrecorded.

## M1 — Synthetic registry and controlled survey intake (NEXT)
- [ ] Specify versioned person, role, submission, commodity and location schema.
- [ ] Develop deterministic generator targeting 50,000 farmer and 5,000 processor **roles**; verify distinct-person and overlap policy.
- [ ] Inject ground-truth-labelled duplicate/invalid/missing scenarios; preserve raw submissions.
- [ ] Implement Pandera validation with missing/null/type tests.
- [ ] Capture source metadata, sample design, codebook, licence and hash **before** using actual public survey files.
- [ ] Define geographic datasets/rights and restrictions before map work.

## M2 — Data engineering
- [ ] Relational schema and migrations, dbt SQL models, DuckDB reconciliation.

## M3 — Quality, identity and governance
- [ ] DQ rules, human-reviewed identity issues, provenance and disclosure testing.

## M4 — Analytics and dashboards
- [ ] Power BI and Streamlit with validated metrics, safe spatial aggregations.

## M5 — Optional AI
- [ ] Read-only question-answering go/no-go and evaluation.

## M6 — Release and portfolio
- [ ] Clean reproducibility, CI, benchmarks and optional owner-approved publication.

**Next:** M1-01 schema and synthetic data specification.
