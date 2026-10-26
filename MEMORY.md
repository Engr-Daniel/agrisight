# MEMORY.md — AgriSight context
Updated 2026-10-26.

- Private repository Engr-Daniel/agrisight, default master. Owner Oyewale Daniel; assistant mentors a structured analytics learning project.
- Independent of confidential Petgrave.io/Arzikin Noma Africa projects. No real registration or farmer dataset is represented.
- Separate permitted survey microdata from clearly labelled synthetic registration demonstrations; never merge their population totals.
- M0 initial documentation and draft ADRs merged under PR #1, commit bef7cf5.
- M0-04 introduces a six-role **synthetic** unit test: submitted 6, accepted roles 4, distinct accepted persons 3, farmer roles 2, processor roles 2, complete accepted 3, incomplete accepted 1. One person has two roles.
- Python and SQLite implement independent calculations checked against manual expected values; 9 targeted tests observed passing in an isolated local Python run. Full repository CI and Ruff checks not yet verified.
- These are test examples, not empirical agricultural findings or performance benchmarks.
- Proposed stack: Python/SQL, PostgreSQL, DuckDB, dbt, Pandera or GX Core, Power BI, Streamlit, GeoPandas/PostGIS, pytest and CI. Advanced AI optional.
- M0 still open: source codebook/licence review, real quality schemas, architecture owner sign-off, privacy model, clean checkout and CI verification.
- Next: actual sources and proof-of-concept validation framework, then formal M0 review.
