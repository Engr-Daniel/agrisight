# CP1 delivery review

Date2026-10-31. Scope: the owner's “proceed” instruction for the next crop portfolio/diversity increment, followed later by separate seed-source analysis. No whole-site redesign.

## Decisions and implementation

The pre-specified [contract](CROP_PORTFOLIO_CONTRACT.md) narrows eligibility to type1 temporary records in the main-season crop file. The first v1.0 calculation aborted on an unlabelled code. A quality-only diagnostic and explicit v1.1 amendment precede the first successful portfolio run; the155 unlabelled records are confirmed permanent/continuous and excluded. No name/code imputation or replacement with another module's labels. Unknown temporary codes still fail closed.

[Actual findings](../reports/CROP_PORTFOLIO_FINDINGS.md) distinguish480393 source crop rows,380464 eligible temporary rows,349322 household–crop pairs and119909 represented households. Each household counts once per crop across plots. Categories, distribution bins, mean and coverage counters independently agree in Python/SQLite. The12950-household difference from crop participation remains visible and is not automatically interpreted as an error or permanent-only households.

Agricultural Insights now has Crop portfolio / Recorded diversity modes and percentage/count controls, using green horizontal bars and a complete table. The portfolio chart is explicitly limited to ten of43 observed categories. Mean2.91 refers to released temporary categories, not all farms or species. Denominator, season context, permanent exclusions, metadata/coverage limits and supported follow-up accompany results. The optional reviewed adapter fails independently; existing activity, water and map evidence is preserved. The shared bar helper accepts an explicit chart class/count unit, leaving its Water Management default unchanged.

## Executed checks

Initial targeted suite27 passed18.04s: manual across-plot deduplication, duplicate raw rows, missing/orphan keys, invalid/unknown eligible codes/types, allowed unlabelled excluded code, empty/permanent-only universes, SQL disagreement, coverage/mean/bin/share/label/count rejection,5+ bin, hash/core-total mismatch, CLI guards, mode/unit navigation, scope warnings and optional failure. Actual source keys/labels/types and all integer reconciliations passed. Further regression, reproduction and browser checks follow after execution.

## Remaining scope

No national inference, crop-output ranking, complete farm diversity, permanent-crop season claim or geographic crop targeting. Unknown-category scope and roster differences remain disclosed. Seed sources require their own key/code/period and overlap contract; source options use0/1 coding and must not reuse1/2 activity assumptions. M6-04 release/privacy/permission/security work remains open. No new deployment or raw-data publication.

## Regression and reproduction evidence

Full348 tests passed development135.85s and noneditable installed-wheel174.04s; Ruff and pip check pass in both environments. Complete actual CP1 output reproduces byte-for-byte, SHA256 `32a783210eadda2ff72d966088fc0c15cf7f235834f861abfafed4f625495811`. The installed model uses packaged crop-label metadata and SQL; no dependency changes. Final packaging/browser details follow after execution. Minor final presentation change corrects singular ?1 recorded category?; it does not change numbers or eligibility.

## Final browser, package and preservation checks

Actual Chrome audit UTC `stakeholder-browser-20261030T235038Z`, local review date2026-10-31:20 checks passed across50 captures, desktop1440 x1000 and narrow390 x844,0 JavaScript exceptions, loopback request host only, no document/main horizontal overflow, both temporary ports closed and no cleanup notes. Keyboard checks cover crop portfolio/diversity, percentage/household units, exact maize count/share, diversity-bin values/mean and return to portfolio, plus prior activity, water-management and map/table/tooltip flows.

Inspected desktop diversity and narrow portfolio/diversity captures: denominator and scope are above charts, long labels fit, top-ten subset and distinct-household interpretation are visible. A final singular-label grammar correction (?1 recorded category?) changes no numeric content; source and final installed-wheel crop/irrigation targeted52 tests passed13.88s/15.99s afterward. The full348-pass regression results precede that wording-only change; no additional full run is claimed for it.

Final wheel SHA256 `9105811843529f689657e9b9579496fbd34a33144e0c2b0b915090eaf7cb3170`; new modules, SQL, label metadata and manifest verified in wheel. Model/SQL/contract/labels/lock hashes and document links checked. All prior survey/synthetic, SA1, GC1 and IR1 artifact hashes remain unchanged. Raw data and new JSON remain ignored. Workspace8501 preview restarted after verifying its command line; health200 observed; preview intentionally stays running. No new deployment, public hosting, survey redistribution or remote-CI result is claimed.
