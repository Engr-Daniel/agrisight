# Architecture and introduction gates

Updated: 2026-10-29. Staged implementation of existing engineering goals; no full platform is implemented.

## First analytical workflow

Authorized immutable inputs in ignored local storage → Python inspection and source-specific validation → documented transformations → independently checked indicators → reproducible report.

Survey and synthetic data use separate directories, contracts and outputs. Survey relationships must come from documentation; the synthetic person/role model is not imposed on a household or plot survey. Flag unusual observations for review; never silently delete or overwrite them.

| Component | Responsibility | Introduction gate / verification |
|---|---|---|
| Python, pytest, Ruff, existing CI | scripts and automated checks | Reproduce the foundation locally under Python 3.11+ |
| Pandas | source inspection and tabular processing | Select and lock when source formats are known |
| Pandera | initial schema/quality library where useful | Source-specific rules and edge cases; not a completed survey integration |
| Jupyter | optional exploration and teaching | Reusable logic stays in tested modules; clear outputs before sharing |
| DuckDB / SQL / Parquet | transformations and independent reconciliation | Introduce for selected files/queries; document types and join cardinality |
| Survey-statistical implementation | design-aware estimates and uncertainty | Verify design support and validate methods before population inference; library not yet selected |
| PostgreSQL | persistent relational storage and constraints | Demonstrated persistence, relational or concurrent access need; migration/integration checks |
| dbt | managed SQL models, lineage and tests | Repeated transformation graph warrants it; keep one versioned authoritative metric definition |
| PostGIS / GeoPandas | justified spatial processing | Licensed geography, CRS, sample support and disclosure review |
| Power BI or Streamlit/Plotly | communicate checked findings | Choose one first; reconcile filters/totals; add another for a distinct purpose |
| Docker | runtime packaging | Demonstrated environment/deployment need |
| Advanced analytics / AI | optional later capability | Explicit need, baseline comparison and separate evaluation |

No new framework or CI infrastructure is required by this review. Great Expectations remains a comparison experiment, not a second core validator. Dependency locks cover the chosen increment, not the whole proposed stack.

## Supporting synthetic entity model

Opaque person IDs link to actor-role entries; submissions and approval events are separate concepts. Commodity associations are many-to-many. Optional farm, enterprise, location, quality-issue and audit entities require contracts before implementation. Acceptance and completeness are separate in the fixture, not an approved enrollment policy.

Keep raw events immutable and record corrections. Evaluate labelled duplicate candidates against known truth; repeated keys alone are not person matching. Test multiple workload sizes, retaining 55k role entries as a selected workload rather than a universal scale threshold.

## Decision references

Implemented M2 increment: [NASS-01 staging → eligibility → mart model](NASS01_MODEL.md) uses ephemeral SQLite with an independently checked Python reference. Packaged SQL is versioned; no persistent service is introduced. This is the current authoritative implementation of the first sample indicator, not competing definitions in a dashboard.

- [ADR-001](adr/ADR-001-stack-and-grain.md): historical stack/grain baseline and current staging amendment.
- [ADR-002](adr/ADR-002-geography-and-privacy.md): geographic and privacy boundaries.
- [ADR-003](adr/ADR-003-validation-choice.md): initial Pandera selection with limited comparison evidence.
- [Review alignment](REVIEW_ALIGNMENT.md): rationale, benefit, trade-offs and verification.

## M4 presentation decision

[ADR-004](adr/ADR-004-initial-reporting-platform.md) selects Streamlit for a local read-only prototype. The [reporting contract](M4_REPORTING_CONTRACT.md) limits it to validated aggregate artifacts with separate survey/synthetic views. No Streamlit dependency is installed by the decision; adapter/schema, locked installation and UI checks are next. Other component gates remain active.
