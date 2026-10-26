# Project Charter — draft for M0 sign-off

## Context
Agricultural programmes may require structured registries, reliable field data, coverage monitoring and operational insights. Incomplete, duplicated or geographically inconsistent records can undermine decisions. AgriSight will **demonstrate** solutions using openly permitted research data and separate explicitly synthetic operations data.

## Purpose and scope
Produce a traceable pipeline from documented data sources and synthetic registration events to verified quality metrics, geographic analysis and management dashboards.

**In scope:** documented requirements, data contracts, synthetic profiling, SQL/dbt models, quality and identity evaluation, privacy-aware spatial aggregates, Power BI and Streamlit, end-to-end testing, performance reports.

**Out of scope:** enrolling real farmers, field deployment, claiming impacts on production/livelihoods, identifying households, storing personal contact details, representing any client system, promising geographic granularity unsupported by samples.

## Personas and decision examples (hypotheses awaiting review)
- Programme manager: Which areas or activities appear underserved according to *appropriately supported* evidence?
- Supervisor: Where do submitted records require quality review?
- Registry admin: Which person-role candidates need a manual identity-resolution decision?
- Analyst: How were a chart's numerators, denominators and filters constructed?
- Governance lead: Can a sensitive attribute or precise location leak through filtered views?

## Provisional research/engineering questions
RQ1: Can a documented workflow handle 55,000 synthetic registration **entries** with consistent role accounting?
RQ2: How accurately do deterministic/risk-based controls catch injected errors and duplicate candidates?
RQ3: Are displayed KPIs reproducible from the same underlying model across tools?
RQ4: How do spatial precision and privacy aggregation affect valid reporting?
RQ5 (optional): Can safe natural-language queries deliver correct answers without unsupported claims?

## Proposed quality gates — require approval
- Reproducible seeded data and deterministic expectations.
- Referential and uniqueness constraints hold; cross-tool KPI tests agree on defined fixture cases.
- Quality detector evaluation reports precision/recall and false-positive trade-offs.
- No raw synthetic PII-like fields in released screenshots; public survey conditions obeyed.
- Benchmarks include hardware, input rows, execution settings, repeated trials and limitations.
- Metrics always identify grain, time window, missingness, role-overlap policy and weight use.

## Stakeholder acceptance
Sign off in a future `docs/M0_REVIEW.md` after explicit evaluation of scope, risks, data source licences, metrics and architecture; this draft is **not yet approved**.
