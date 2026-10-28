# M0 completion review — AgriSight
**Date:** 2026-10-27
**Outcome:** Design baseline accepted for M1 synthetic-track implementation; external-data integration remains gated.

## Purpose and interpretation
M0 determines **what to build, for whom, how success is assessed, and what evidence is required**. It does not require us to implement the full registry, access restricted survey microdata, or prematurely optimize performance. The owner requested completion of M0 on 2026-10-27; the decisions below are the documented **working baseline**, revisable through ADRs. This is not a signature or proof of explicit line-item owner approval.

## Exit checklist
| Gate | Evidence | Disposition |
|---|---|---|
| Stakeholder questions | `docs/M0_DECISION_QUESTIONS.md` | COMPLETE as proposed use-case baseline; not user-interview validated |
| Scope, outcomes, acceptance strategy | `docs/PROJECT_CHARTER.md`, `docs/M0_ACCEPTANCE_CRITERIA.md` | COMPLETE as engineering hypotheses |
| Registration grain and states | `docs/adr/ADR-001-stack-and-grain.md`, this review | BASELINE ACCEPTED for synthetic track |
| Data sources and sampling boundaries | `docs/M0_SOURCE_ASSESSMENT.md`, `docs/M0_SOURCE_DECISION.md` | COMPLETE for source-selection gate; file-level inspection moved to M1 |
| KPI definitions and executable independent checks | `docs/KPI_DICTIONARY.md`, `docs/M0_KPI_LAB.md` | CORE KPI CONTRACT COMPLETE; advanced indicators are M1+ |
| Validation choice | `docs/M0_05_COMPARISON_REPORT.md`, `docs/adr/ADR-003-validation-choice.md` | PAN DERA FIRST (provisional operational evaluation) |
| Verification | Foundation CI run 40495776063; comparison run 40495776119 | PASSED for seven tiny synthetic scenarios; not a benchmark |
| Privacy, geographic limitations and licensing gates | `docs/M0_PRIVACY_THREAT_MODEL.md`, ADR-002 | DESIGN GUARDRAILS COMPLETE; actual boundary licensing deferred to map acquisition |
| Formal owner line-by-line signature | This file | NOT COLLECTED; future explicit ratification remains recommended |

## Agreed **working assumptions** to build upon
1. Each `person_id` is an opaque simulated identity; a person can have both farmer and processor roles.
2. `role_id` identifies an individual assigned actor role, **not** a unique human. Model 50k farmer roles + 5k processor roles as a **synthetic role-entry target**; distinct-person total may be below 55k.
3. Submission status is `pending`, `accepted` or `rejected`. Quality status is a separate concept and never silently overrides approval. A profile may be accepted yet incomplete in our demonstration.
4. `accepted_role_count` and `distinct_accepted_person_count` are separate KPIs, verified against a manually calculated fixture.
5. The **canonical metric definitions** will be versioned in the transformation layer; DuckDB/Python provide independent reconciliation; Power BI and Streamlit must not calculate competing denominators.
6. The initial synthetic demo is privacy-safe, using opaque IDs, coarse/artificial geography and no actual names, phones, GPS coordinates or client data.
7. Official sample-survey analysis is **separate** from simulated operations. Published survey weights/design/geography and permitted file redistribution require examination **before any ingestion**.
8. Choose **Pandera** for Python ingestion contracts initially. Retain dbt tests for relational analytics and reassess GX Core only if documented operational quality reporting demands it.
9. Keep one lightweight foundation CI workflow. Dedicated comparisons are opt-in experiments, not compulsory complexity.
10. Do not claim any actual 55k dataset has been built or real-life farmers registered.

## Post-M0 explicit dependencies
- M1 begins with a schema and seeded data generator; no external survey download is needed to begin **synthetic** modelling.
- External survey lane remains blocked until codebooks, weights, exact release terms, geography and source hashes are checked.
- Map layer remains blocked until legal boundary source, geographic resolution, CRS and disclosure policies are validated.
- Future indicators require separate fixtures/denominator tests before being labeled production-ready.
- The user may revise these defaults at any subsequent design review. The document is a technical gate, not contractual approval.

## Milestone decision
**M0 completed for the synthetic-registry engineering track; M1 ready to start with guarded scope.**
Not evidence of production readiness, field enumeration, full survey processing, validated impact or an approved client proposal.

## 2026-10-28 scope amendment (supersedes M1 ordering only)
The owner clarified that **empirical work using real agricultural data is the primary project objective**. M1 now starts with source access/dictionary review and E1 empirical data profiling. The synthetic 55k role registry is retained strictly as a supporting engineering benchmark in a later workstream. The previous M0 design findings remain useful but do not constitute evidence that survey data have been acquired. See `docs/M1_EXPERIMENT_PLAN.md`. No retrospective changes to prior test results are implied.
