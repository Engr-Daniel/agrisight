# AgriSight
### Agricultural Data Intelligence & Decision Support Platform

**Status:** M0 design foundation complete; M1 source feasibility and E1 profiling next · **Repository:** private · **Owner:** Oyewale Daniel

AgriSight is an independent, learning-oriented portfolio project combining **empirical agricultural intelligence** with **trustworthy analytics delivery**. Research establishes what authorized agricultural data support; engineering makes those findings reproducible and useful through validated pipelines, SQL models and reporting.

It is not an operational farmer registry, a deployed client system or evidence of field enrollment. Official observations, derived indicators, synthetic records and mock-ups must always remain distinguishable.

## Purpose and intended users

Analysts and programme managers need to understand agricultural patterns without hiding missing data, uncertain estimates or geographic limitations. Data administrators need traceable transformations and quality checks; governance reviewers need privacy-aware reporting. These are proposed personas, not completed user interviews. Synthetic operational demonstrations additionally support supervisor and registration-review use cases.

## Goals

1. Select authorized real agricultural data against explicit research questions and documented feasibility.
2. Produce defensible agricultural indicators with clear units, denominators, reference periods, weights, uncertainty and limitations.
3. Build reproducible ingestion, SQL transformations, validation and independent numerical checks.
4. Deliver evidence-backed reporting and supported geographic analysis.
5. Evaluate robustness to missing information and reasonable analytical choices.
6. Separately test error detection, identity handling and scale with seeded synthetic data, including a **55,000-role-entry workload** (illustratively 50,000 farmer roles and 5,000 processor roles; not necessarily 55,000 people).
7. Document reproducibility and measured engineering performance; evaluate advanced analytics or a read-only AI analyst only if justified.

## Questions and dataset decision

Candidate questions concern geographic patterns in agricultural participation, differences in input/service access, and sensitivity of findings to analytical assumptions. **None is yet established as answerable.** See the [research feasibility matrix](docs/RESEARCH_FEASIBILITY.md).

Inspect NASS 2023 first. GHS Panel 2023–24 remains a genuine alternative if it better supports the selected question; it is not automatically an extra dataset. Select one source for the first complete analysis after checking variables, access, design, reference periods and geographic support. Never pool survey respondents with synthetic registrations.

## Staged architecture

```text
Authorized survey files (ignored, immutable local inputs)
    → Python inspection and documented validation
    → versioned analytical transformations / SQL
    → independently checked indicators and uncertainty
    → reproducible report → one initial dashboard

Separate synthetic fixtures → controlled engineering evaluation
```

The initial analytical tools may include Pandas, Pandera, DuckDB and Parquet as needed. Pandera is the working validation choice, based on a limited synthetic comparison; survey integration is not yet implemented. Choose and lock dependencies for the next increment.

PostgreSQL/dbt, PostGIS/GeoPandas, Power BI and Streamlit/Plotly remain engineering learning goals, introduced through [documented need and verification gates](docs/ARCHITECTURE.md). Choose one dashboard tool first. No new framework or CI system is needed for this review.

## Roadmap

| Milestone | Focus | Status |
|---|---|---|
| M0 | Design foundation, evidence boundaries, counting and validation fixtures | Complete as foundation only |
| M1 | Source feasibility, permitted acquisition, E1 data suitability/profiling | Next |
| M2 | E2 agricultural findings and tested analytical models | Planned |
| M3 | E3 sensitivity; separate synthetic quality/scale investigations | Planned |
| M4 | Verified interactive reporting and supported geography | Planned |
| M5 | Justified advanced analytics / optional grounded AI | Optional |
| M6 | Reproducibility, benchmarks and owner-authorized portfolio release | Planned |

See [TASK.md](TASK.md), [charter](docs/PROJECT_CHARTER.md), [E1–E3 plan](docs/M1_EXPERIMENT_PLAN.md), [review rationale](docs/REVIEW_ALIGNMENT.md) and [data policy](docs/DATA_POLICY.md).

## Quick start: foundation examples

Requires Python 3.11+. From a checkout:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m agrisight.kpi_fixture
.\.venv\Scripts\python.exe -m agrisight.quality_baseline
```

See [development setup](docs/DEVELOPMENT.md) for other platforms and the analytical dependency-locking gate. These examples use synthetic data; SQL reconciliation uses in-memory SQLite, not an implemented PostgreSQL database.

**Implemented:** package scaffold, six-row Python/SQL KPI fixture, basic non-mutating validator, optional seven-case framework comparison, tests and CI workflows. **Not implemented:** real survey ingestion, empirical findings, 55k generator, operational database, dashboards or deployment.

## Repository navigation

- `AGENTS.md`: collaboration and evidence rules.
- `TASK.md`: actionable state; `MEMORY.md`: confirmed decisions, results and caveats.
- `docs/`: specifications, research plan, review decisions and historical M0 evidence.
- `src/agrisight/`: scaffold and small executable experiments.
- `tests/`: scaffold, KPI and validation checks.
- `data/README.md`: ignored local storage convention; no acquired dataset is included.

## Ethics and reuse

Independent of confidential Petgrave.io/client work. No real PII, precise respondent locations, credentials or restricted downloads in Git. Private visibility is not a substitute for permission or data protection. Preserve source versions and label all outputs. Public code, data or deployment release requires explicit owner authorization; dataset licences may differ from the software licence.

**Author:** [Oyewale Daniel](https://github.com/Engr-Daniel).
