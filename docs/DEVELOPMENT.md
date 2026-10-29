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
