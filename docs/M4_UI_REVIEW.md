# M4-03 Streamlit interface review

Observed 2026-10-29. **M4-03 complete; M4-04 browser/usability and combined milestone review pending.** Headless interaction tests and a healthy HTTP server do not establish visual usability. No public deployment or independent stakeholder acceptance is claimed.

## Implemented scope

The checkout entrypoint [streamlit_app.py](../streamlit_app.py) calls the packaged [reporting UI](../src/agrisight/reporting_ui.py). The UI invokes the existing adapter on every interaction; it does not accept uploaded bundles, mint manifests, cache old evidence, load raw data or execute experiments. Source labels, period, evidence date, actual UTC build timestamp and scientific limits accompany each selected view. Unknown input fields remain excluded by the adapter.

| View | Selections and behavior |
|---|---|
| Survey findings | NASS-01/NASS-02 only; household denominator/exclusions, plot missingness, known-only reference and full-roster bounds remain distinct. Empty/unbounded/recorded-zero cases have separate labels |
| Synthetic quality | All three reserved seeds, three configurations, two baselines, two matching relations and five field-rule/micro choices. Counts, pair/event-rule universe, precision/recall/FPR denominators and undefined-rate reasons stay visible |
| Workload measurements | Four bounded event sizes and two separate collision diagnostics; timing versus traced allocation, all repetitions and median/min/max/sample SD, with a native repetition chart. Rejected cases never appear as zero-valued successful measurements |

Synthetic matching defaults to Mixed/B1/duplicate-role at seed 303 so known weaknesses, rather than an easy perfect case, appear first. Workload defaults to 55000 bounded-group events. These are explicit navigation defaults, not pooled results or claims that these cases are representative. Both remain labelled SYNTHETIC DEMONSTRATION DATA; CI fixture panels instead say TEST FIXTURE.

Formatting follows the contract: percentage two decimals, positive rates below 0.01% shown as `<0.01%`, area two decimals, seconds three decimals, MiB two decimals and integer counts with separators. Full-precision cell data and reviewed source/model fingerprints are inspectable in an evidence expander. No upload, download-bundle, raw-row, map, SQL, experimental rerun or second-dashboard control exists.

## Verification observed

- 36 new parametrized UI tests pass. Their selection loops exercise all 126 quality cells, both survey indicators and all 12 workload/measurement combinations, plus manual golden values, state transitions, undefined/unbounded/zero cases, live input invalidation and safe unavailable messages. They also check repetition tables/chart units and the absence of a chart or measurement card on rejection.
- Known fixture outcomes independently check 66.67% participation, bounds 3/5, mixed matching precision/recall/denominator changes and distinct null/zero display. These are explicitly synthetic aggregate fixtures, not claimed M3 detector results or actual survey findings. Existing pure adapter and analytical tests remain the numerical evidence underneath.
- Full 204 tests passed in `.venv-m4` and against the noneditable installed wheel in `.venv-m4-repro`. Ruff and `pip check` passed. The current dependency locks/pins are unchanged. Existing CI lint now includes the checkout entrypoint; no remote runner result is asserted.
- Actual owner-authorized aggregates were checked separately in headless AppTest: NASS-01 displays 92.84% over 143105 valid households; NASS-02 endpoints 6070.29 labelled m² with width 0; Mixed/B1 duplicate precision 90.91% at 303 and 87.72% at 505, recall 50% and FPR `<0.01%`; 55000-event median 1.071 seconds and 16.65 MiB traced allocation, with 39363 people/47181 intended roles; collision rejection shows499500 potential pairs versus 250000 budget. Private audit `m4_actual_ui_smoke.json` records these checks. The first ad-hoc PowerShell probe needed an escaped superscript label because of console encoding; no UI/source change was needed.
- Runtime settings were inspected in installed Streamlit 1.66.1: loopback 127.0.0.1, headless mode, usage statistics disabled, error details hidden and minimal toolbar. The checked-in [configuration](../.streamlit/config.toml) contains no secrets or external assets. These settings are defaults, not authentication or an authorization system; CLI/environment overrides must be reviewed before sharing.
- A separate hidden local test process started on an automatically selected loopback port. `/_stcore/health` returned 200/`ok` and the root returned HTTP 200. That process tree was stopped and its port verified closed. Private audit `m4_server_smoke.json` records startup/shutdown. HTTP requests establish only server/shell availability; they do not execute a browser or validate rendered layout.

The package includes the UI module alongside the adapter/manifest and no restricted inputs. The root launcher/config are checkout files; this prototype is run from the repository root, not a standalone hosted release. Bare-mode ScriptRunContext warnings during AppTest did not cause app exceptions.

## Run locally and next review

After the [M4 dependency setup](DEVELOPMENT.md), from the checkout root:

```powershell
.\.venv-m4\Scripts\python.exe -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true --browser.gatherUsageStats false
```

Open `http://127.0.0.1:8501` locally and stop the process with Ctrl+C. The verification server was stopped; no live preview is left running by this checkpoint. Missing or changed inputs show unavailable panels; no production-looking fallback dataset is substituted.

M4-04 must review layout/readability, source/limitation visibility, keyboard interaction, chart/table legibility and narrow-window behavior in an actual browser when tooling is available, then record the combined M4 handoff and any fixes. No browser screenshot, visual usability inspection or stakeholder review was performed in M4-03. Keep scientific/geography/access gates active even after eventual prototype closure.

## M4-04 follow-up

The [combined M4 review](M4_REVIEW.md) now closes the local prototype after actual Chrome desktop/narrow checks and internal visual inspection. Earlier pending statements describe their historical stage. Broader browser/user validation and release authorization remain outside this completion.
