# AgriSight
### Agricultural Data Intelligence & Decision Support Platform

**Status:** M1 — real agricultural data acquisition and first empirical profiling experiment (planned) · **Repository:** private · **Owner:** Oyewale Daniel

AgriSight is an independent, reproducible portfolio and learning project exploring how agricultural survey and synthetic registration data can be transformed into **trustworthy indicators, geographic insights, operational monitoring, and actionable decisions**. It is **not** an operational farmer registry, a deployed client system, or evidence that field profiling has occurred.

> **Evidence boundary:** Official survey observations, synthetic registrations, derived indicators, and illustrative mock-ups must always be labelled separately. Never represent simulated records as real farmers, field work, or survey findings.

## Problem and intended users
Large registration programs encounter duplicate entries, missing answers, inconsistent locations, fragmented records, and dashboards that conceal data-quality limitations. AgriSight prototypes an auditable workflow for:
- **Programme managers:** coverage, progress, commodities and intervention targeting.
- **Field supervisors:** submission patterns, exceptions, verification queues.
- **Data administrators:** schemas, validation, auditability, controlled corrections.
- **Analysts:** traceable KPI definitions, spatial summaries, reproducible reports.

## Goals
1. Model a scalable **55,000-record synthetic demonstration** (illustratively 50,000 farmer roles and 5,000 processor roles; person/role overlap handled explicitly).
2. Ingest permitted public survey data with documented source, licence, weights, geography and limitations.
3. Build tested SQL transformations and transparent metric definitions.
4. Evaluate data completeness, validity, duplication and geographic anomalies.
5. Deliver management and data-quality dashboards with geographic drill-down.
6. Benchmark correctness and performance and publish reproducible methodology.
7. Optionally evaluate a **read-only**, evidence-grounded natural-language analyst.

## Architecture (proposed, subject to M0 ADR approval)
```text
Public anonymized survey data        Labelled synthetic registrations
                \                   /
                 Python ingestion / Parquet
                          |
             PostgreSQL (+ PostGIS as needed)
                          |
        dbt models / tests / documented metrics
                          |
             Quality & geospatial checks
                          |
          ┌───────────────┴──────────────┐
      Power BI report              Streamlit/Plotly
          └────────── Reporting & evidence ───────────┘
    DuckDB for independent file-based exploration and validation
```
Build the smallest trustworthy vertical slice first. Avoid adding unnecessary infrastructure.

## Proposed stack
Python, SQL, PostgreSQL/PostGIS, DuckDB, dbt, Pandas, GeoPandas, pytest, Power BI, Streamlit/Plotly, GitHub Actions and Docker. Choose one primary validation framework after evaluation (Pandera or GX Core). Optional later: FastAPI, scikit-learn, SQLGlot, an LLM API. Versions and licensing must be assessed before adoption.

## Data strategy (revised 2026-10-28)
**Primary track: real agricultural data.** Begin with officially documented Nigerian agricultural surveys; inspect access terms, questionnaire/codebook, survey design, weights, missing-value codes and geographic support before analysis. First experiment E1 profiles actual authorized data quality and variable availability; do not invent findings or treat a sample as a census.

**Supporting track: synthetic registry engineering.** Use seeded, labelled simulations only to test identity handling, quality detection, system scale and software correctness. Never pool simulated entries with real survey respondents.

The current 55,000-entry objective is a synthetic **engineering stress-test target**, not the principal empirical dataset or evidence of field registrations. See [M1 protocol](docs/M1_EXPERIMENT_PLAN.md).

## Roadmap
| Milestone | Focus | Status |
|---|---|---|
| M0 | Charter, evidence policy, research questions, ADRs, development environment | **In progress** |
| M1 | Public data discovery, provenance, synthetic registry specification | Planned |
| M2 | PostgreSQL schema, ingestion, transformations, semantic metrics | Planned |
| M3 | Validation, duplication benchmark, quality monitoring, privacy controls | Planned |
| M4 | Power BI, Streamlit, geographic and quality dashboards | Planned |
| M5 | Optional evidence-grounded analyst and safety/evaluation | Planned |
| M6 | CI, performance benchmarks, documented release, shareable sanitized demo | Planned |

See [TASK.md](TASK.md), [project charter](docs/PROJECT_CHARTER.md), [architecture decisions](docs/ARCHITECTURE.md), and [data policy](docs/DATA_POLICY.md).

## Quick start (scaffold only)
Requires Python 3.11+.
```bash
git clone https://github.com/Engr-Daniel/agrisight.git
cd agrisight
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
python -m agrisight
```
The command prints the scaffold status. **No ingestion, dashboard, or database is implemented yet.**

## Repository navigation
- `AGENTS.md`: rules for human/AI collaborators and change validation.
- `MEMORY.md`: durable decisions, boundaries, status, unresolved questions.
- `TASK.md`: milestone tasks, objective acceptance criteria, evidence.
- `docs/`: charter, architecture, data policies, KPI design and contribution guide.
- `src/agrisight/`: minimal package bootstrap.
- `tests/`: scaffold smoke tests.

## Ethics and reuse
This project is independent of Petgrave.io client work. Do not upload any client data, private materials, names, phone numbers, precise home/farm locations, access tokens, or confidential deliverables. Survey data must comply with their access and reuse terms. Private repository visibility does **not** substitute for data protection.

**Author:** [Oyewale Daniel](https://github.com/Engr-Daniel). The software repository includes a license; **dataset licences may differ**.
