# ADR-001 — Minimal analytics architecture and entity grain
**Decision status:** Proposed, pending owner approval (2026-10-26).

## Context
A reproducible flagship analytics project must demonstrate relational registry modelling and independent analytical checks without needless platform complexity.

## Proposed decisions
1. **Person** is a synthetic opaque identity. A person can have zero or more **actor roles** (farmer and/or women processor). Registration targets refer to *role entries* in the first implementation, not automatically distinct humans.
2. **Submission event** (including failed validation) differs from accepted role record; counts expose this distinction.
3. **Raw public survey observations remain isolated** from synthetic operational registration tables. Cross-system comparison is narrative/analytic, not a naive UNION.
4. **PostgreSQL** is the operational and transformation-backed store; PostGIS introduced only where justified.
5. **dbt** is the canonical transformation and data-test layer with models producing curated reporting views.
6. **DuckDB** is a local exploratory and independent reconciliation engine, not a second authoritative registration database.
7. **Power BI** is the management BI artifact; **Streamlit** is the private interactive demonstration based on certified curated metrics, not an independent competing KPI engine.
8. **Python** is for generation, ingestion, non-SQL checks and evaluation; pytest and CI test executable contracts.
9. Select **one** primary schema-validation framework after small comparable proof of concept. No LLM required until independent M5 go/no-go.

## Trade-offs
- PostgreSQL + dbt + DuckDB creates some overlap; reduce duplication by assigning canonical metrics to dbt only.
- Power BI and Streamlit show distinct audiences but should share metrics and check totals.
- Person/role separation is extra schema complexity needed to avoid double counts.

## Alternatives rejected *provisionally*
- One flat 55k-row spreadsheet: hides identity and change-history problems.
- One monolithic Streamlit script: hard to test lineage and metric definitions.
- Cloud orchestrator, Spark or Kubernetes: unnecessary at this scale.
- LLM-first design: risk of unsupported or inaccurate claims.

## Review gates
Approve/adjust based on implementation costs, available computing resources, integration compatibility and learner feedback. No architecture has been tested yet.
