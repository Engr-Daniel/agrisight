# MEMORY.md — AgriSight durable project context
Updated 2026-10-28.

## Direction
Owner: Oyewale Daniel; private repository Engr-Daniel/agrisight, single master branch.
**Priority correction:** real-world agricultural analysis is the MAIN objective. Synthetic registration data is strictly a supporting engineering test fixture/stress test, not the main analytical dataset. The previous M1 synthetic-first plan is superseded; see docs/M1_EXPERIMENT_PLAN.md.

## Completed M0
Design foundation and seven-case validation comparison. Foundation CI and Pandera/GX Core experimental runs passed on prior commits. No real survey files yet inspected at variable level, no real empirical experiment run, no dashboard, no 55k generator or real registrations. Experimental findings must not be fabricated.

## Next M1
NASS 2023 official survey documentation and permission review; permitted data acquisition without repository redistribution; codebook and survey design inspection; then E1 real-data profiling. GHS Panel is a secondary candidate. Confirm survey sampling weights and supported geographic domains before prevalence inference.

## Supporting engineering track
Use seeded synthetic role registrations for deduplication and scale checks in M3, with labels and strict separation. Person and actor-role remain separate keys. Pandera initially chosen for Python ingest contract; PostgreSQL/dbt/DuckDB and BI later when justified.

## Boundaries
Independent of confidential Petgrave.io/client work. No personal identifiers, real precise coordinates, secrets or restricted downloads in Git. No public release without owner consent.
