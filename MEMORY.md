# MEMORY.md — AgriSight durable project context

Updated: 2026-10-28.

## Direction

Owner: Oyewale Daniel; private repository Engr-Daniel/agrisight; stable integration branch master. On 2026-10-28 the owner explicitly requested merging and proceeding without unnecessary new branches; continue this increment on master with scoped commits and checks.

AgriSight combines empirical agricultural intelligence with trustworthy analytics delivery. Real-data research is primary; pipelines, SQL modelling, quality, statistics, supported geography and reporting remain engineering goals. Synthetic records provide separate known-truth and scale experiments, never population evidence. M0 remains complete as a foundation, not full user validation or empirical completion.

## Existing evidence

The repository records prior foundation CI and seven-case Pandera/GX runs. The six-row synthetic fixture independently checks Python/SQLite counts; the basic validator reports issues without changing records. Pandera remains the initial working choice; comparison evidence is limited to tiny synthetic cases. Initial source-documentation inspection is now recorded below; full downloaded-file feasibility remains open. No respondent microdata acquisition, agricultural findings, dashboard, operational database, 55k generator or deployment exists.

## Review decisions — 2026-10-28

- Owner authorized targeted file updates after discussing the review. Work is on `feat/m1-review-alignment`; no reopening M0, wholesale stack replacement or additional CI infrastructure.
- Current charter/README state both objectives. E1 suitability is M1; E2 agricultural analysis is M2; E3 sensitivity is M3, alongside separate supporting engineering studies.
- RQ1 geographic agricultural participation, RQ2 input/service access differences, RQ3 sensitivity are candidates only. Exact variables and methods remain unverified.
- Inspect NASS first. GHS is a genuine alternative if better supported by feasibility evidence, not automatically supplementary. Select one source for the first complete workflow. See `docs/RESEARCH_FEASIBILITY.md`.
- Stage PostgreSQL/dbt/spatial/dashboard tools through demonstrated need. Select and lock dependencies for the next actual analytical increment; no analytical lock or survey-statistical library has been chosen.
- Current plans supersede historical synthetic-first ordering. Notices preserve original decisions and test evidence. Rationale/benefit/trade-off/verification are recorded in `docs/REVIEW_ALIGNMENT.md`.
- Ignore all local `data/` contents except its README, plus private reports. Tiny reviewed synthetic fixtures remain in source/tests. No downloads were performed.

## Observed local verification — 2026-10-28

- `py --list` revealed Python 3.11 alongside the default 3.10. Created ignored `.venv` with `py -3.11 -m venv .venv`; interpreter reports Python 3.11.9.
- Initial sandbox dependency installation could not resolve build requirements; the authorized network-enabled retry of `.\.venv\Scripts\python.exe -m pip install -e '.[dev]'` succeeded. Observed pytest 9.2.0 and Ruff 0.17.3. This is a foundation environment, not a locked analytical environment.
- `.\.venv\Scripts\python.exe -m pytest -q`: **19 passed**.
- `.\.venv\Scripts\python.exe -m ruff check src tests`: **All checks passed**.
- `git check-ignore --no-index` identified representative raw/interim/curated/synthetic data, private reports and `.venv` paths as ignored. `git ls-files data` contained only `data/README.md`.
- Ad hoc documentation checks passed for relative links in all 18 changed/new Markdown files, and negative ignore checks confirmed source files, the feasibility document and data README remain trackable. `git diff --check` passed.
- This increment changes documentation/storage rules, not application behaviour; no implementation-mirroring tests or new CI were added.

## Boundaries and next handoff

No confidential Petgrave.io/client materials, identifying locations, secrets or restricted downloads in Git. No public release or deployment without owner authorization. Flag unusual values rather than silently deleting them; unknown is not automatically no; survey weights alone do not establish valid confidence intervals.

Next: authenticated NBS access terms/file inventory, release/design reconciliation, analytical dependency locking and permitted acquisition. Do not mark feasibility, E1 or statistical methods verified merely because the plan exists.

## Merge and initial source inspection — 2026-10-28

- Fetched origin, fast-forwarded master to alignment commit `b4d4fb8`, and successfully pushed master at the owner's request. No reset, force push or branch deletion.
- Inspected NBS catalogue/JSON/access page, relevant public questionnaire sections, World Bank mirrored NASS household/plot/input dictionaries, the FAO access route and GHS metadata. Sources and exact findings are in `docs/data_sources/NASS_2023_CARD.md`; feasibility matrix now records narrowed/deferred questions instead of blank planning rows.
- Downloaded only the public NBS questionnaire (981956 bytes, 61 pages) into ignored storage. SHA256 `29a696d9764a1d8c70874a18d4e0b4d5f8d4b2d2ba6d8a7efaeabbd17ac4f676`. Extracted relevant pages with inspection-only pypdf 6.21.3 installed locally; no change to core dependencies. Initial console extraction hit Windows encoding limits; UTF-8 output/extraction succeeded.
- NBS dictionary endpoint timed out; mirrored World Bank dictionary provided exact names. Mirrored release is not presumed byte/schema-identical to an unseen NBS download. Some individual-variable endpoints failed; no categories inferred from unavailable pages.
- `final_weight` is listed in the mirrored household/plot dictionaries; its applicability and released variance-design information remain unverified. Do not substitute the listing weight from catalogue prose.
- Proposed first E1 field: main-season plot irrigation infrastructure `s02_q07`, documented codes 1=yes, 2=no. Infrastructure presence is not input/service access. No sample proportions or population estimates were computed.
- NBS microdata requires login; World Bank routes to FAO, which routes to NBS. Actual authenticated terms/files remain pending. No account creation, login, acceptance of terms or respondent-file download was attempted. GHS remains an alternative, with variable-level matching incomplete.
- Verification after inspection updates: 19 existing tests passed, Ruff passed, `git diff --check` passed, relative links in all five changed/new documents resolved, and downloaded/extracted questionnaire paths were confirmed ignored. No source-documentation claim is treated as an executed empirical result.
