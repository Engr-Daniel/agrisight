# MEMORY.md — AgriSight
Updated: 2026-10-26.

- Private repository Engr-Daniel/agrisight. Owner Oyewale Daniel. Work on master for now; mentor-guided engineering approach.
- Independent of Petgrave.io client confidential materials. Synthetic registration data and official sampled survey observations never pooled as a real census.
- M0-04 verified tiny synthetic fixture: six submissions; four accepted roles, three distinct accepted persons.
- M0-05 dependency-free validation baseline and official NASS/GHS catalogue-level review previously committed; no original microdata or variable-level codebooks ingested yet.
- Proposed stack: Python, SQL, PostgreSQL/PostGIS, dbt, DuckDB, one primary Python data validation framework, Power BI and Streamlit. AI optional.
- Pandera vs GX Core preliminary experiment executed successfully: GitHub Actions run 40355059389 on a2a4ba6, Python 3.11, pandas 2.3.3, pandera 0.35.0, GX 1.24.1; both passed valid data and rejected invalid fixture. GX still omits empty-string/strict-bool checks; comparison is not semantic parity. Foundation lint error on a2a4ba6 was corrected and foundation CI passed on 61f1104.
- Official docs: https://pandera.readthedocs.io/en/latest/dataframe_schemas.html and https://docs.greatexpectations.io/docs/core/introduction/try_gx/
- M0 pending actual comparison, source files/access audit, KPIs, privacy, review/sign-off.
