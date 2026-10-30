# Development environment

The package requires Python 3.11+. On Windows, `python` may select an older installation even when 3.11 exists. Check the interpreter explicitly.

## Foundation setup

From the repository root in PowerShell:

```powershell
py --list
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/e1.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e '.[dev,e1]'
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m agrisight.kpi_fixture
```

On Linux/macOS, create the environment with `python3.11 -m venv .venv` and use `.venv/bin/python` for the remaining commands. Activation is optional when invoking the environment interpreter directly.

## E1.1 pinned environment

The initial Stata-reading increment is resolved in `requirements/e1.lock`: runtime, test and editable-build dependencies, excluding inspection-only PDF tooling. To reproduce in a fresh Python 3.11 environment:

```powershell
py -3.11 -m venv .venv-e1-repro
.\.venv-e1-repro\Scripts\python.exe -m pip install -r requirements/e1.lock
.\.venv-e1-repro\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e '.[dev,e1]'
.\.venv-e1-repro\Scripts\python.exe -m pip check
.\.venv-e1-repro\Scripts\python.exe -m pytest -q
.\.venv-e1-repro\Scripts\python.exe -m ruff check src tests
.\.venv-e1-repro\Scripts\python.exe -m agrisight.e1_profile data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/e1_1_reproduced.json
.\.venv-e1-repro\Scripts\python.exe -m agrisight.e1_suitability data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/e1_2.json
```

The archive must already exist in ignored storage; CI uses synthetic tests only. The existing foundation CI now installs this lock and the selected extra; no new workflow is added. Version pins are not artifact hashes or an offline dependency bundle. Fresh installation is verified on Windows/Python 3.11.9 only; do not claim Linux or GitHub runner results until observed. For Linux/macOS substitute `.venv-e1-repro/bin/python`.

## Reproducibility gate for later M1 work

The base foundation keeps dependency ranges; use the increment lock above for E1.1. Before expanding the analysis:

1. Select dependencies required by the chosen source formats and checks; optional exploration notebooks do not replace executable scripts.
2. Record exact direct/transitive versions in a reviewed lock or reproducible requirements artifact and document the installer/platform. Keep research-only comparison dependencies separate.
3. Verify installation into a fresh Python 3.11+ environment, run tests/lint and the analytical commands, and record observed versions/results.
4. Select a survey-statistical implementation only after checking actual design requirements and verifying its methods. Do not silently substitute ordinary standard errors.

Do not preinstall PostgreSQL, dbt, spatial tools, both dashboard tools or a new framework for source documentation inspection. See MEMORY.md for results actually observed in this workspace.

## M2 NASS-01 and package verification

E2 adds no dependency; reuse `requirements/e1.lock` and the selected extra above. From the repository root:

```powershell
.\.venv\Scripts\python.exe -m agrisight.nass01 data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/nass01.json
.\.venv\Scripts\python.exe -m pip wheel --no-build-isolation --no-deps . --wheel-dir reports/private/wheels
.\.venv-e1-repro\Scripts\python.exe -m pip install --no-deps --force-reinstall reports/private/wheels/agrisight-0.0.1-py3-none-any.whl
.\.venv-e1-repro\Scripts\python.exe -m pip check
.\.venv-e1-repro\Scripts\python.exe -m pytest -q
.\.venv-e1-repro\Scripts\python.exe -m agrisight.nass01 data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/nass01_reproduced.json
```

The second environment now runs the installed wheel, not its previous editable checkout. Source/SQL resources are packaged via `pyproject.toml`; verify complete parsed JSON equality between the two outputs, including provenance. Windows Python 3.11.9/Pandas 2.3.3/SQLite 3.45.1 were observed; a different platform may change provenance or float details and must be evaluated rather than claimed bit-identical. Wheels remain ignored private artifacts. Model/lock hashes identify the exact bytes used; do not report a successful run's old output as evidence after a failed rerun.

## M3 NASS-02 empirical bounds

Reuse the unchanged E1 lock. Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m agrisight.nass02 data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/nass02.json
```

Repeat the wheel build/install and checks above, then run the same module with `.venv-e1-repro` and output `reports/private/nass02_reproduced.json`. Compare complete parsed JSON, including provenance. Both environments passed77 tests and reproduced exactly on Windows/Python3.11.9. SQL is packaged; CI requires only synthetic fixtures. Outputs remain ignored; the source hash and field labels are guarded. See the [contract](NASS02_INDICATOR_CONTRACT.md) for support assumptions and fail-fast cases.

## M3-04 synthetic accuracy

Reuse the current lock; no new dependencies. Run development seeds first and freeze the source/protocol/contract hashes before evaluation. The [protocol](experiments/M3_04_PROTOCOL.md) fixes seed/configuration and mutation choices. Commands and actual metrics are in the [findings/review](../reports/M3_SYNTHETIC_QUALITY.md).

```powershell
.\.venv\Scripts\python.exe -m agrisight.synthetic_quality --phase development --output reports/private/m3_04_development.json
.\.venv\Scripts\python.exe -m agrisight.synthetic_quality --phase evaluation --output reports/private/m3_04_evaluation.json
```

Build/install the wheel using the M2 commands above, then run the evaluation with `.venv-e1-repro` and output `reports/private/m3_04_reproduced.json`; complete parsed JSON should match in the observed pinned Windows environment. This regenerates fictional rows in memory, passes observation-only records to the detector, and writes only aggregate results and provenance. No survey input or external account is needed. The CLI output guard rejects paths outside ignored `reports/private`. `generate` has a deliberately fixed1000-person accuracy workload; performance scaling is a separately versioned M3-05 task.

## M3-05 local workload measurements

The [benchmark protocol](experiments/M3_05_PROTOCOL.md) fixes workload generation, timed scope, repeats, Python-allocation measurement and rejection handling before execution. Reuse the current lock; no new dependency. From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_workload_benchmark.py -q
.\.venv\Scripts\python.exe -m agrisight.workload_benchmark --output reports/private/m3_05_benchmark.json
```

The suite launches sequential fresh workers (120-second timeout each). Input generation, imports, hashing and process startup are outside reported batch time. Five repetitions measure time; three separate repetitions measure peak traced Python allocation after input generation, not total RAM or RSS. Avoid concurrent build/test work when seeking isolated comparisons; disclose shared-machine load. Do not compare profiler elapsed times with uninstrumented timings. Full suites are manual experiments, never speed assertions in CI.

For a packaged smoke check, build/install the wheel using the instructions above and invoke the installed module's `--worker --size 55000 --mode timing`; compare input/truth/prediction hashes and counts with the suite reference, not machine-dependent elapsed time. Row-level tokens/truth remain in memory; only reviewed aggregates belong in Git. The pair-budget wrapper is scoped to this module and does not change direct M3-04 detector behaviour.

## M4-02 reporting dependency and adapter environment

`requirements/m4.lock` pins Streamlit1.66.1 and its resolved dependencies together with all unchanged analytical/test/build pins from `e1.lock`. Observed Windows Python3.11.9 only; lock pins do not include wheel hashes or guarantee another platform. The existing CI installs this lock, optional reporting extra and synthetic tests; do not claim a remote result before observing it.

```powershell
py -3.11 -m venv .venv-m4
.\.venv-m4\Scripts\python.exe -m pip install -r requirements/m4.lock
.\.venv-m4\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e '.[dev,e1,reporting]'
.\.venv-m4\Scripts\python.exe -m pip check
.\.venv-m4\Scripts\python.exe -m pytest -q
.\.venv-m4\Scripts\python.exe -m ruff check src tests
.\.venv-m4\Scripts\python.exe -m agrisight.reporting_adapter --output reports/private/m4_bundle.json
```

The adapter reads only the four fixed reviewed aggregates, never raw microdata, and fails dependent panels on missing/mismatched inputs. The command writes current unavailable states and exits1 rather than retaining stale success. It refuses output outside ignored reports/private or over an evidence input. Review the [schema](M4_BUNDLE_SCHEMA.md) before changing the manifest; do not automatically re-sign altered artifacts. Test fixtures are explicitly labelled and require no actual evidence files.

For clean package reproduction:

```powershell
py -3.11 -m venv .venv-m4-repro
.\.venv-m4-repro\Scripts\python.exe -m pip install -r requirements/m4.lock
.\.venv-m4\Scripts\python.exe -m pip wheel --no-build-isolation --no-deps . --wheel-dir reports/private/wheels
.\.venv-m4-repro\Scripts\python.exe -m pip install --no-deps --force-reinstall reports/private/wheels/agrisight-0.0.1-py3-none-any.whl
.\.venv-m4-repro\Scripts\python.exe -m pip check
.\.venv-m4-repro\Scripts\python.exe -m pytest -q
.\.venv-m4-repro\Scripts\python.exe -m agrisight.reporting_adapter --output reports/private/m4_bundle_reproduced.json
```

Compare installed dependency maps and all parsed bundle fields except genuine run-specific built_at_utc; validate both timestamps as UTC instead of fabricating a shared build time. The adapter/manifest are packaged resources. The existing .venv and E1 lock remain untouched. No dashboard launch command exists yet; M4-03 implements that interface after these checks.

## M4-03 interface and interaction checks

Use the M4 lock/extra above; no additional dependency is required. From the checkout root:

```powershell
.\.venv-m4\Scripts\python.exe -m pytest tests/test_reporting_ui.py -q
.\.venv-m4\Scripts\python.exe -m pytest -q
.\.venv-m4\Scripts\python.exe -m ruff check src tests streamlit_app.py
.\.venv-m4\Scripts\python.exe -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true --browser.gatherUsageStats false
```

The launcher/config live in the checkout; the UI module is packaged. Open http://127.0.0.1:8501 on the same machine; stop with Ctrl+C. Explicit flags preserve local binding and disabled telemetry even if global settings differ. Do not remove those limits for sharing without a separate deployment/access review. The entrypoint derives its root from its own file, and never accepts browser root/manifest inputs.

Every widget interaction rebuilds the validated bundle; no session-state evidence fallback or artifact cache exists. AppTest uses patched offline fixture loading with TEST FIXTURE origins. It does not require actual authorized inputs in CI. Pure analytical environments without the optional Streamlit dependency skip the UI test module; use the M4 environment for the full reporting regression suite. Bare-mode ScriptRunContext warnings can appear in headless tests; check actual AppTest exceptions/results instead of inferring a browser session from logs.

A local HTTP health check proves server availability, not browser rendering. See [M4-03 verification](M4_UI_REVIEW.md) for what was observed and remaining browser/usability work. Earlier M4-02 statements that no launch command existed describe that stage; the launcher is now implemented.

## Internal browser review

Run `.\.venv-m4\Scripts\python.exe scripts/m4_browser_review.py` with installed Chrome (or `--browser PATH`) and reviewed local aggregates. No new dependency is needed. The helper launches an isolated fresh profile, uses temporary loopback ports, records source fingerprints and 19 captures privately, and stops its own processes. Review screenshots separately. This is native Chrome rendering, distinct from AppTest; it is not a CI browser job or a physical-device/accessibility study. See the [combined review](M4_REVIEW.md) for observed results and limits.

## M6 clean-source audit

See the [reproduction protocol](M6_REPRODUCTION_PROTOCOL.md) and [observed audit with commands](M6_REPRODUCTION_REVIEW.md). A fresh source export/environment passes all 204 tests but exposes line-ending-sensitive historical provenance. Keep raw-byte hashes truthful; do not normalize/re-sign old evidence silently.

## Versioned text and provenance

The [policy](PROVENANCE_POLICY.md) and [migration review](M6_PROVENANCE_REVIEW.md) resolve the synthetic lane's raw-byte hash portability using .gitattributes. Keep that file in clean exports. Text uses LF; frozen locks and historical manifest v1 retain exact reviewed CRLF bytes. The active adapter loads snapshot v2; historical survey/workload entries have not been regenerated. Use the same commands above, retain ignored historical outputs and compare complete synthetic JSON. The M6-01 observed hash mismatch remains historical evidence, not the current synthetic status.

## Authorized survey clean reproduction

The [M6-03 protocol](M6_SURVEY_REPRODUCTION_PROTOCOL.md) and [observed review](M6_SURVEY_REPRODUCTION_REVIEW.md) add the real-input lane. Export the frozen commit from the repository root, build/install its wheel using the unchanged lock, and run agrisight.nass01 and agrisight.nass02 with an absolute path to the separately stored frozen authorized archive. Keep outputs beneath each checkout's reports/private. Verify complete parsed JSON and raw hashes, not only displayed rounded values. The observed outputs match the existing manifest v2, so no manifest change is required. CI remains fixture-only; its Linux success does not establish actual survey reproduction on Linux.

## Dashboard presentation assets

The [visual refresh](DASHBOARD_VISUAL_REVIEW.md) packages assets/dashboard.css and assets/agricultural-landscape-v1.webp with the wheel. No asset CDN or font download is needed. Artwork generation/prompt is documented in [asset provenance](ILLUSTRATION_ASSETS.md). Only decorative resources are memoized; restart the development server after asset-only edits. Evidence validation remains uncached. Browser review now checks that the actual packaged image decodes and fingerprints the style/asset files. The audit helper attempts all owned process cleanups and records unconfirmed exits; existing owner-run previews are not its cleanup targets.

## Two-layer navigation

The app now defaults to the stakeholder Overview. Agricultural insights and Engineering studies link to exact Evidence & methods selections; About explains the prototype. See the [presentation contract](TWO_LAYER_PRESENTATION.md) and [verification](TWO_LAYER_REVIEW.md). State callbacks persist navigation only; summary figures always come from the freshly validated bundle. The browser helper tests both layers and expects a fresh reload to open Overview. Its narrow drawer handling scrolls back to the header before closing. Restart an existing preview after updating the app to ensure old sessions/modules do not mask the new default experience.
