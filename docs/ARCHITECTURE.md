# Architecture — candidate design, not implemented

## Responsibilities
| Component | Responsibility | Validation |
|---|---|---|
| Python/Pandas | source parsing, synthetic generation, ingestion | schema, deterministic tests |
| PostgreSQL | normalized operational store, relationships, migration-based schema | constraints, SQL integration tests |
| PostGIS | optional permitted spatial indices/query logic | CRS and boundary validation |
| dbt | canonical staging/intermediate/marts SQL transformations | model, relationship, accepted-value tests |
| DuckDB | exploratory analysis, Parquet and independent metric reconciliation | independently computed fixtures |
| Quality library (TBD) | data contract/rule checks | induced failures and error examples |
| Power BI | semantic measures, enterprise report prototype | DAX vs authoritative SQL reconciliation |
| Streamlit/Plotly | private demonstrator, controlled filters and reports | UX and permission tests |
| pytest / GitHub Actions | reproducible local and CI checks | observed jobs, versioned artifacts |

## Entity model (candidate)
- `person`: synthetic, opaque person key. No phone/email/name required for public demonstration.
- `actor_role`: person key, type (`farmer`, `processor`), status, effective date; **role count differs from person count**.
- `farm`, `enterprise`, `person_site_link`: optional many-to-many geographic/operational assignments.
- `location`: administrative hierarchy and approved aggregate geographies.
- `submission`: raw immutable intake event with instrument version, consent simulation indicator, batch, time.
- `verification_event`: review, findings and human-approved decisions.
- `quality_issue` and `audit_event`: rule code, source, severity, status and corrective history.
- `commodity` and association tables: explicit multi-value commodity relationships.

## Data flows
Raw landing zone (immutable) → validated operational records → versioned analytics models → verified KPI views → reports. Different data origins get separate namespaces, schemas or datasets; **never union them into one population total**.

## Design issues / ADR backlog
ADR-001: PostgreSQL vs DuckDB responsibilities and canonical metrics.
ADR-002: person-role overlap and target-grain definition.
ADR-003: GIS geography/CRS, spatial precision and privacy thresholds.
ADR-004: primary data quality library (Pandera vs GX Core).
ADR-005: BI model integration and power-bi artifact release.
ADR-006: synthetic data distributions and injectible ground truth.
ADR-007: optional LLM analyst access policy and SQL safety.

## Non-goals at initialization
No deployed architecture, orchestrator, authenticated user model, infrastructure-as-code, API, production monitoring or LLM service is claimed. All require independent implementation and validation.
