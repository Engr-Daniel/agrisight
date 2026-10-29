# AgriSight
### Agricultural Data Intelligence & Decision Support Platform

**Status:** M0-M3 complete within scoped objectives; M4 reporting specified, implementation pending · **Repository:** private · **Owner:** Oyewale Daniel

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

Candidate questions concern geographic agricultural participation, input/service access and sensitivity to analytical assumptions. E1 now supports a narrowed first workflow: **main-season crop participation in the observed sample**. Population inference remains gated by design verification; a dry-season year conflict excludes cross-season comparison. See [observed E1 findings](reports/E1_REAL_DATA_PROFILING.md), [feasibility decisions](docs/RESEARCH_FEASIBILITY.md) and [M1 technical review](docs/M1_REVIEW.md).

E2 independently reconciles that first indicator: **132859 / 143105 eligible released household records = 92.84%** reporting main-season crop growing. This is unweighted sample description, not national prevalence. See [E2 findings](reports/E2_AGRICULTURAL_FINDINGS.md), [SQL model](src/agrisight/sql/nass01.sql) and [M2 review](docs/M2_REVIEW.md).

E3 bounds the full released main-season plot-roster median at **6070.29 in the labelled square-metre units**. The 48 missing entries cannot shift that median under the nonnegative-value completion model because bounding ranks are tied. This does not establish measurement accuracy or national plot size. See [E3 findings](reports/E3_PLOT_AREA_BOUNDS.md) and [contract](docs/NASS02_INDICATOR_CONTRACT.md). [Synthetic quality evaluation](reports/M3_SYNTHETIC_QUALITY.md) is now complete: normalization improves repeat detection but retains missed pairs and false links. [Workload measurements](reports/M3_WORKLOAD_BENCHMARK.md) now include55000 events: median1.07 seconds for the specified local batch, with16.65 MiB peak traced Python allocation (excluding existing inputs/native memory). Shared-machine timings and bounded-key inputs do not establish production capacity. See the [M3 review](docs/M3_REVIEW.md).

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

Streamlit is selected for the initial local, read-only evidence explorer; its dependency lock and implementation remain pending. The [platform decision](docs/adr/ADR-004-initial-reporting-platform.md) and [reporting contract](docs/M4_REPORTING_CONTRACT.md) define separate survey/synthetic views and only supported aggregate selections. PostgreSQL/dbt, spatial tools and a second dashboard tool retain [demonstrated-need gates](docs/ARCHITECTURE.md); no deployment is included.

## Roadmap

| Milestone | Focus | Status |
|---|---|---|
| M0 | Design foundation, evidence boundaries, counting and validation fixtures | Complete as foundation only |
| M1 | Source feasibility, acquisition, E1 profiling and suitability decision | Complete for scoped baseline; M2 restrictions documented |
| M2 | NASS-01 sample finding and tested analytical model | Complete for first approved workflow; inference gates retained |
| M3 | E3 readiness and conditional next-indicator study; separate synthetic investigations | Complete for empirical bounds, synthetic accuracy and scoped workload studies |
| M4 | Verified aggregate reporting; geography separately gated | In progress: Streamlit decision/contract; implementation pending |
| M5 | Justified advanced analytics / optional grounded AI | Optional |
| M6 | Reproducibility, benchmarks and owner-authorized portfolio release | Planned |

See [TASK.md](TASK.md), [charter](docs/PROJECT_CHARTER.md), [E1–E3 plan](docs/M1_EXPERIMENT_PLAN.md), [review rationale](docs/REVIEW_ALIGNMENT.md) and [data policy](docs/DATA_POLICY.md).

## Quick start: foundation examples

Requires Python 3.11+. From a checkout:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/e1.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e '.[dev,e1]'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m agrisight.kpi_fixture
.\.venv\Scripts\python.exe -m agrisight.quality_baseline
```

See [development setup](docs/DEVELOPMENT.md) for other platforms and the analytical dependency-locking gate. These examples use synthetic data; SQL reconciliation uses in-memory SQLite, not an implemented PostgreSQL database.

**Implemented:** synthetic counting/validation exercises; bounded E1 source profiling; independently reconciled Python/SQL NASS-01 participation and NASS-02 missing-area median bounds; pinned environment, packaged models, measured synthetic batch workloads, tests and existing CI. **Not implemented:** full ingestion/analytics pipeline, population estimates, operational database, dashboards or deployment. Restricted inputs are never required for CI.

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
