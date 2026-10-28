# ADR-003 — Python validation framework
Status: **Accepted as working M1 baseline** (2026-10-27), subject to empirical review at scale.

> Scope clarification (2026-10-28): the comparison evidence below concerns synthetic fixtures only. Pandera remains the initial choice where useful for real-data source contracts, with rules derived from inspected documentation. This does not establish survey suitability or a completed ingestion integration. Synthetic generator work is supporting and later; M1 begins with source feasibility.

## Decision
Use **Pandera** for code-first synthetic registration ingestion contracts. Supplement with relational constraints and dbt tests once the database layer exists. Do not bring Great Expectations into the core dependency graph unless a need for managed expectations/reporting emerges.

## Evidence
GitHub comparison: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776119
Versions logged: Python 3.11, Pandas 2.3.3, Pandera 0.35.0, GX Core 1.24.1. Valid synthetic example accepted by both; six invalid cases rejected by both. This is **pass/reject agreement on tiny cases**, not comprehensive semantic parity, high-volume validation, diagnostics or performance superiority.

## Rationale
M1 needs small, version-controlled dataframe schemas. A local Pandera schema is adequate; carrying both tools would introduce duplication before we have an operational need. We prioritize fewer dependencies and clear testable contracts.

## Consequences
- Begin M1 with a clear schema and validation tests in Pandera.
- Retain lightweight Python checks as independent expectations and teaching material.
- Check nullable columns, mixed dtypes, missing columns, coercion, null treatment and structured failure cases in M1.
- Reconsider if distributed validation, richer reporting, or different data backends become necessary.
