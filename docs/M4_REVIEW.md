# M4 combined technical review

Date: 2026-10-29. **Complete for a local, read-only evidence explorer.** This is internal engineering review, not external stakeholder acceptance or release authorization.

## Acceptance evidence

- M4-01: [reporting contract](M4_REPORTING_CONTRACT.md) and [platform decision](adr/ADR-004-initial-reporting-platform.md) define three separate evidence views and scientific/access gates.
- M4-02: [adapter review](M4_ADAPTER_REVIEW.md) verifies the pinned environment, reviewed aggregate manifest, strict validation and installed-wheel reproduction.
- M4-03: [UI review](M4_UI_REVIEW.md) verifies automated interactions. The 36 UI cases exercise all 126 quality cells, both survey indicators and 12 workload/measurement choices, plus failure/transition states.
- M4-04: real headless Chrome/156.0.8078.49 on Windows rendered desktop 1440x1000 and narrow 390x844 CSS viewports. Six checks passed over 19 captures: keyboard indicator/view/seed selection, collision rejection, narrow navigation/provenance and no page-wide horizontal overflow. Zero JavaScript exceptions were recorded. Observed tab request hosts were only 127.0.0.1; this is not a system-wide network audit. Both temporary server/debugger ports were closed after cleanup.

The final source-fingerprinted audit is ignored at `reports/private/m4_browser_review/20261029T183034829792Z/review.json`. Its automatic status deliberately leaves visual inspection separate. `visual_inspection.json` records the internal visual inspection, including selected final captures and additional captures from the preceding successful run with the same product code. Tables, charts, denominator labels, repeated source captions and expanded provenance were legible in the inspected captures. Local scrolling inside provenance is permitted; page-wide overflow was checked at every capture.

Earlier probes exposed incomplete-render waits and browser-driver navigation/key-event issues. The driver now waits for completed reruns/charts and sends native key characters. Failed private audits are retained; these were not product navigation fixes or performance experiments.

## Changes and regression evidence

Observed presentation issues led to repeated source captions beside tables/charts, survey warnings scoped to the selected indicator, shorter human-readable UTC build times and source/unit chart alternative text. Full timestamps remain in evidence. Analytical inputs, metric definitions, manifest and dependency pins are unchanged.

After the product changes, 36 targeted UI tests passed; all 204 tests passed in development (17.55 seconds) and the noneditable installed-wheel environment (18.84 seconds). Ruff and pip check passed. The rebuilt wheel SHA-256 is `32cbc0edac3e6857f5c984d1b89fed27f0e760a078fa8053e852882bb359a4db`. Existing CI includes the browser helper in lint, but no new remote CI/Linux result is claimed. Browser execution is a separate manual local check and requires reviewed ignored aggregates.

## Repeating the browser check

After the [M4 setup](DEVELOPMENT.md), run:

```powershell
.\.venv-m4\Scripts\python.exe scripts/m4_browser_review.py
```

Supply `--browser PATH` if Chrome is elsewhere. The helper uses the existing locked websockets dependency, a fresh isolated private browser profile and temporary loopback ports. It retains logs/screenshots under ignored storage and stops its own processes. Inspect representative screenshots separately; an automated pass cannot establish visual usability by itself.

## Limits and handoff

This covers one installed Windows Chrome version and two viewport sizes, not physical touch devices, other browsers, screen-reader testing, formal accessibility certification or representative user research. AppTest provides wider selector coverage than the browser sampling. No server remains running.

Survey sample/measurement limitations, source separation, unavailable evidence behavior and geographic/privacy gates remain active. No raw-data browser loading, new experiment, operational registry, public deployment or publication permission is implied. Next is M6 clean-checkout reproduction and release-readiness review; M5 advanced analytics remains optional and needs a justified question.
