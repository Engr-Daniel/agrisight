# MEMORY.md — AgriSight durable context
Updated 2026-10-26.

## Project identity
Private repository: `Engr-Daniel/agrisight` (default `master`). Owner: Oyewale Daniel. Mentored hands-on portfolio in agricultural data intelligence, database engineering, quality controls, geospatial analytics, BI and rigorous evaluations.

## Confirmed
- Private-first; explicit authorization required before any public code/data/demo release.
- Independent of confidential Petgrave.io and Arzikin Noma Africa client work.
- No field registration or real farmer profiles claimed.
- Public survey analysis and 55k synthetic operational *role entries* are different data families and cannot be naively pooled.
- No raw client material, personal identifying data or precise farm coordinates should be committed.
- AGENTS.md governs disciplined small increments with explanations and evidence.

## M0 work produced (drafts, not owner-approved)
- Decision inventory: `docs/M0_DECISION_QUESTIONS.md` (10 questions, proposed personas).
- Acceptance criteria: `docs/M0_ACCEPTANCE_CRITERIA.md`.
- Source metadata audit: `docs/M0_SOURCE_ASSESSMENT.md`.
- Architecture & grain proposal: `docs/adr/ADR-001-stack-and-grain.md`.
- Location/privacy proposal: `docs/adr/ADR-002-geography-and-privacy.md`.
- No public microdata actually downloaded, no survey-weight code audited, no real dashboard, no generator, and no working architecture demonstrated yet.

## Metadata findings (2026-10-26)
- NASS 2023 household sample survey, with multistage weighting and anonymized released microdata. Precise GPS/address identifiers withheld and geography below LGA suppressed in anonymized distribution. Source: https://microdata.worldbank.org/catalog/8194 and https://microdata.nigerianstat.gov.ng/index.php/catalog/173.
- GHS Panel 2023–24 is a national/zone representative household panel (~5,000 households) under a research data licence, **not** a complete farmer registry or necessarily an LGA-resolution dataset. Source: https://datacatalog.worldbank.org/search/dataset/0066579/nigeria-general-household-survey-panel-2023-2024.
- Actual dataset access permissions, released variables, consent scope, geography and weights remain to be checked before ingestion.

## Proposed technology only
Python, SQL, PostgreSQL/PostGIS, DuckDB, dbt, one of Pandera/GX Core, Power BI, Streamlit/Plotly, pytest, Docker, GitHub Actions. No cloud infrastructure or AI system yet.

## Next
M0-04: validate microdata file permissions & codebook, KPI math test fixtures and minimal actual execution. M0 stays open until evidence and owner sign-off.
