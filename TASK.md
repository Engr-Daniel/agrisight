# TASK.md — AgriSight roadmap
Updated: 2026-10-28

## M0 — Engineering research foundation (COMPLETE, with revised M1 priority)
- [x] Stakeholder decision questions, architecture options and provenance/privacy rules.
- [x] Seven synthetic-registration KPI contracts and independent Python/SQL fixture tests.
- [x] Pandera vs GX Core seven-case comparison; CI evidence: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776119
- [x] Pandera-first decision for initial Python validation.
- [x] Record correction: **real survey empirical analysis is primary; synthetic work is supporting only**.
M0 establishes a design baseline, not an empirical result or a final user-study approval.

## M1 — Real agricultural data: acquisition and Experiment E1 (NEXT)
- [ ] M1-01: inspect NASS 2023 official catalogue, all relevant questionnaires and downloadable codebooks.
- [ ] M1-02: record actual licence/access conditions, study version, file inventory and analysis permissions.
- [ ] M1-03: acquire permitted microdata in a **local ignored directory**, record hashes and provenance; never commit restricted files.
- [ ] M1-04: identify observational unit, survey strata/PSU/weights, geographic limits, missing codes and relevant variables.
- [ ] M1-05: execute E1 reproducible data profiling (rows, schema, missingness, duplication, invalid values) on actual permitted records.
- [ ] M1-06: compare chosen quality rules, document exclusions and baseline findings; distinguish sample descriptive summaries from weighted population estimates.
- [ ] M1-07: add tests, reviewed findings, limitations and clear report before closing M1.

## M2 — Analytics engineering (PLANNED)
- [ ] PostgreSQL/dbt models, SQL KPI definitions and independent reconciliation for approved real-data analysis.

## M3 — Robustness and supporting registry experiments (PLANNED)
- [ ] Controlled seeded synthetic records to benchmark 55k role entries, duplicate detection and quality controls. No simulated counts presented as real observations.

## M4 — Evidence-backed reporting (PLANNED)
- [ ] Power BI and Streamlit dashboards grounded in authorized real-data findings; synthetic-only operational demonstrations explicitly separated.

## M5 — Advanced analytics (OPTIONAL)
- [ ] Evaluate advanced statistics or evidence-grounded AI only if justified.

## M6 — Publication and reproducibility (PLANNED)
- [ ] Independent checks, CI, measurement reports, licensing/privacy review and approved portfolio release.

**Immediate next:** M1-01 official source documentation inspection. See docs/M1_EXPERIMENT_PLAN.md.
