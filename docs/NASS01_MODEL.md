# NASS-01 analytical model v1.0

Implemented 2026-10-29 under [indicator contract](NASS_INDICATOR_CONTRACT.md) and [E2 protocol](experiments/E2_PROTOCOL.md). Only the narrowed sample indicator is authorized by this model.

| Layer | Grain and purpose | Contract |
|---|---|---|
| Source | Household records in frozen NASS ZIP | Hash checked; fixed member and selected fields only; raw input unchanged |
| `stg_nass_households` | One row per released household | Non-null unique normalized household key; raw numeric activity code or NULL retained |
| `int_nass01_eligibility` | Same household grain | Classify missing/yes/no/invalid explicitly; no deletions or join expansion |
| `mart_nass01` | One aggregate row | Numerator, valid denominator, exclusions, proportion, percentage; empty denominator NULL |

The [SQL implementation](../src/agrisight/sql/nass01.sql) is the versioned model definition. It is packaged with the Python application and executed locally in SQLite memory. Identifiers are never persisted to a database, logs or aggregate output. The runner requires source period strings to match the contract; it fails on unexpected periods or ambiguous keys.

## Independent numerical check

The Python reference aggregates original selected response values separately from SQL's CASE expressions and views. Compare all seven integer counts exactly and both rates at absolute tolerance 1e-12. Shared Stata reading and identifier/missing normalization mean this is independent arithmetic/model evaluation, not independent source acquisition or an entirely separate preprocessing implementation. Synthetic cases establish known truth beyond merely requiring two implementations to agree.

Integer calculations are not rounded. SQL uses REAL division and NULLIF; Python uses undefined/null for zero eligible records. Missing and invalid counts remain visible even when zero. No weight, CI, significance test or geographic filtering is silently introduced.

## Lineage and access

Private JSON records archive hash/member, model and contract versions, SQL/model-code/dependency-lock hashes, Python/Pandas/SQLite versions, period, grain, formula, exclusions, weight status and scope. No row IDs, per-geography cells or arbitrary source text are exported. Display rounding belongs to the reviewed report, not the calculation.

The dependency lock is the unchanged `requirements/e1.lock`; E2 adds no packages. Invoke from the repository root so the lock and ignored report area are explicit. A packaged-wheel run in the previously clean reproduction environment checks SQL-resource inclusion and output agreement against the editable development run. The built wheel stays in ignored private storage.

## Architecture introduction decision

**Rationale/benefit:** one source, one household fact and two simple views need no persistent service; versioned SQL, constraints and independent checks demonstrate the relevant engineering responsibilities now.

**Trade-off:** SQLite memory is not multi-user storage or managed dbt lineage. PostgreSQL/dbt remain valid later learning goals when persistence or transformation-graph complexity warrants them. This increment introduces neither service, new framework, orchestration nor CI workflow.

**Verification:** synthetic constraint/denominator/type/period/output tests, actual source run, wheel contents check, independent SQL/Python agreement, packaged-versus-editable reproduction and full test/lint suite. Existing CI runs synthetic tests only; it does not reproduce restricted-data findings.
