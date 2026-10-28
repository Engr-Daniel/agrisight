# Development environment

The package requires Python 3.11+. On Windows, `python` may select an older installation even when 3.11 exists. Check the interpreter explicitly.

## Foundation setup

From the repository root in PowerShell:

```powershell
py --list
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m agrisight.kpi_fixture
```

On Linux/macOS, create the environment with `python3.11 -m venv .venv` and use `.venv/bin/python` for the remaining commands. Activation is optional when invoking the environment interpreter directly.

## Reproducibility gate for M1

The foundation uses dependency ranges, not an application lock. This setup alone does not establish a reproducible analytical environment. Before E1 execution:

1. Select dependencies required by the chosen source formats and checks; optional exploration notebooks do not replace executable scripts.
2. Record exact direct/transitive versions in a reviewed lock or reproducible requirements artifact and document the installer/platform. Keep research-only comparison dependencies separate.
3. Verify installation into a fresh Python 3.11+ environment, run tests/lint and the analytical commands, and record observed versions/results.
4. Select a survey-statistical implementation only after checking actual design requirements and verifying its methods. Do not silently substitute ordinary standard errors.

Do not preinstall PostgreSQL, dbt, spatial tools, both dashboard tools or a new framework for source documentation inspection. See MEMORY.md for results actually observed in this workspace.
