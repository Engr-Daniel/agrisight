# MEMORY.md — AgriSight durable project context
Last updated: 2026-10-26

## Identity
- Project: **AgriSight — Agricultural Data Intelligence & Decision Support Platform**.
- Owner and learner: Oyewale Daniel (GitHub: `Engr-Daniel`).
- Repository: `Engr-Daniel/agrisight`; **private**, default branch `master`.
- Objective: flagship portfolio + structured hands-on learning in modern analytics engineering, GIS, quality, SQL, BI and evaluation.
- Collaboration: assistant acts as **mentor/reviewer**, explaining reasons and requiring reproducible evidence.

## Confirmed commitments
- Private-first development; no publication or public deployment without explicit owner consent.
- Independent project, **not** a reproduction of a proprietary Petgrave.io client system.
- Real permitted anonymized official survey data and clearly labelled synthetic operational profiles will have separate provenance and analysis paths.
- No real PII, confidential client information, or unnecessary precise location data.
- 55,000 registration entries is a **synthetic demonstration target**, not an achievement or real field registration.
- Documentation files required: `README.md`, `AGENTS.md`, `TASK.md`, `MEMORY.md`.
- Complete milestones only when independently verifiable evidence exists.

## Proposed, NOT approved technology decisions
Python/SQL, PostgreSQL(+PostGIS), DuckDB, dbt, one quality framework (Pandera or GX Core), Power BI, Streamlit/Plotly, pytest, Docker, GitHub Actions. LLM integration is optional M5. Formalize architectural choices in ADRs before binding integrations.

## Current state
- M0 documentation and skeletal Python packaging are being initialized.
- **No operational pipeline, validated public dataset, 55k generator, dashboard, benchmark, or deployment exists yet.**
- CI results and clean-install reproduction are not yet verified at initialization.
- Next: M0-01 business/user questions and measurable acceptance criteria.

## Open design questions
1. Do 50,000 farmers + 5,000 processors mean roles, distinct persons, or both? What if a person qualifies twice?
2. What geographic resolution can be legitimately supported by public survey datasets?
3. Which metrics require survey weights and uncertainty intervals?
4. What quality acceptance thresholds are defensible (completeness, suspected duplicates, back-check rates)?
5. What is the minimum defensible set of KPI definitions and dashboard questions?
6. Which transformations belong in PostgreSQL/dbt versus DuckDB? Which metric layer is canonical?
7. Is a public runnable app possible using only generated and approved data, with no secret-bearing backend?
8. Is an AI analyst worth the risk/complexity relative to traditional BI?

## Working log
- 2026-10-26: Owner created private repository and requested full foundation including AGENTS/TASK/MEMORY. Initial scaffold drafted; **implementation remains planned**.

## Update protocol
After each accepted milestone: record decisions (with rationale and date), evidence links, commands/tests actually run, blockers, known limitations and next work. Don't overwrite uncertainty with invented certainty. Avoid storing personal secrets.
