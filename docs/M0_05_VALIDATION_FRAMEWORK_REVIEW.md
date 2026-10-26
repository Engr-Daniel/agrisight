# M0-05 — Data validation framework evaluation
Date: 2026-10-26. **Status: provisional recommendation / incomplete live comparison.**

## Question
Which primary validation framework best fits AgriSight's Python ingestion and early-stage, reproducible analytics pipeline?

## Current documented capabilities
| Dimension | Pandera | Great Expectations (GX Core) |
|---|---|---|
| Core orientation | Schema and dataframe validation in Python | Data-quality expectations, validation definitions/results and orchestration |
| Fit for early project | Good for concise typed pandas checks and custom column/cross-column constraints | Good for mature validation workflows, expectation suites, checkpoints and validation reporting |
| Reporting/ops | Failure cases and programmable error handling | Structured results, checkpoints, actions and Data Docs |
| Complexity in early M1 | Likely lower for pandas-centric local scripts | More components to manage, especially for persisted validation configurations |
| Future value | Strong local contract layer | Potentially useful when data-quality governance, monitoring and shareable validation documentation become central |

**Recommendation (not benchmark result):** adopt **Pandera provisionally** as the first validation library for M1 because the earliest deliverable is a small, code-first pandas ingestion and synthetic data pipeline. Keep GX Core as a candidate for later validation observability, and use SQL/dbt constraints for database models. Avoid using both indiscriminately.

Official docs reviewed:
- Pandera schemas: https://pandera.readthedocs.io/en/latest/dataframe_schemas.html
- Pandera supported backends: https://pandera.readthedocs.io/en/stable/
- GX Core workflow: https://docs.greatexpectations.io/docs/core/introduction/gx_overview/
- GX Core getting started: https://docs.greatexpectations.io/docs/core/introduction/try_gx/

## Executable baseline in this commit
`src/agrisight/quality_baseline.py` and `tests/test_quality_baseline.py` use **standard-library Python**, not Pandera or GX. They establish a reusable expected-error contract:
- required non-empty person and role identifiers;
- role and status controlled vocabulary;
- duplicate role-key detection;
- strict boolean type (integer 1 is not accepted as boolean);
- reporting issues without mutating original submissions;
- deliberate multi-role person permitted.

Test on good and intentionally defective **synthetic** records. Never interpret defects as real field data.

## Current comparison limitation
Environment had pandas/pytest but **neither Pandera nor Great Expectations installed**. Package installation was attempted and failed because the runner had no network resolution to the Python package index. Therefore **no comparative execution, performance, error-report or compatibility result is claimed**.

## Next practical comparison (required before decision sign-off)
1. Use an environment with package-index access and record Python/pandas/Pandera/GX versions.
2. Translate the same baseline contract into each library's current API; no semantics changed.
3. Run identical valid, missing-column, invalid-category, duplicate-key and null tests.
4. Compare error detail, maintainability, serialization, CI integration and (optional) timing on 100/10k synthetic rows.
5. Record failure logs, trade-offs and final choice in an ADR before marking framework assessment completed.

## Risk
The baseline's `complete` flag is educational; future registration instruments require detailed per-field and skip-logic checks. The baseline does not address consent, row-level permissions, privacy suppression, or probabilistic matching.
