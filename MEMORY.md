# MEMORY.md — AgriSight durable context
Updated 2026-10-26.

## Project
Private repository Engr-Daniel/agrisight; development directly on master. Owner Oyewale Daniel; ChatGPT acts as learning mentor. Independent of confidential Petgrave.io/client data.

## Boundaries
Official NBS agricultural survey observations and 55,000 synthetic intended registration-role entries are separate data families. No genuine farmer profiling has been done. No personally identifiable data or actual farm coordinates to be committed. Private visibility does not waive licensing/privacy requirements.

## Verified progress
- M0 design questions, charter, evaluation proposals and ADRs drafted.
- M0-04 six-role synthetic fixture (4 accepted roles, 3 distinct persons) with independent Python/SQLite KPI reconciliation and tests.
- M0-05 official NBS NASS 2023 / GHS Wave 5 catalogue summaries, with dates, licences and representativeness cautions.
- M0-05 standard-library quality contract, test fixtures for required IDs, categories, duplicate role keys and invalid booleans committed.
- Literature/docs comparison favors Pandera provisionally for initial code-first data validation, with GX Core retained as an alternative for future operational validation reporting.

## Unverified and open
- Pandera/GX libraries were absent in the available local environment; pip install failed for lack of package network access, so no head-to-head benchmark was run.
- Variable-level DDI/codebook, actual microdata, weights, licences for each released file, and GIS reporting resolution remain unverified.
- Check new GitHub Actions run before claiming CI success.
- Data model/status decisions and framework selection still require M0 sign-off.

## Next
Execute both framework prototypes in a provisioned environment; inspect released questionnaires and variable-level documentation; finalize M0 acceptance decisions.
