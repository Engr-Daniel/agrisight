# M4-02 dependency and aggregate-adapter review

Observed 2026-10-29. **M4-02 complete; dashboard implementation and M4 closure remain pending.** No app server, browser review, deployment or current GitHub CI result is claimed here.

## Changes and evidence

- Selected Streamlit 1.66.1 after checking [official PyPI metadata](https://pypi.org/pypi/streamlit/1.66.1/json) (Python >=3.11) and actually installing it with all existing E1 pins retained. `requirements/m4.lock` records 45 runtime/test/build distributions including the installer. The old `requirements/e1.lock` is unchanged; the new lock is a strict version superset. Pins are not artifact hashes or an offline wheel archive.
- Created separate `.venv-m4` and clean `.venv-m4-repro` environments, both ignored. Resolved/installed the increment in the first; installed the resulting full lock in the second. Installed distribution name/version maps match exactly, including all 45 pins, plus the local application. Verified Windows/Python 3.11.9 only; Linux CI is configured, not claimed observed.
- Added a pure standard-library adapter and packaged, reviewed aggregate artifact manifest. A bundle has 2 survey,126 synthetic quality and6 synthetic workload records, with independent panel statuses, source context and provenance. [Exact schema/trust boundary](M4_BUNDLE_SCHEMA.md), [reporting contract](M4_REPORTING_CONTRACT.md).
- Added 45 synthetic fixture tests/cases covering known truth, zero/undefined/unbounded/recorded-zero cases, negative/boolean/inconsistent counts, invalid rates/ranks/statuses, incomplete/wrong experiment cells, worker/summary mismatches, invalid hash encoding, missing/corrupt/mixed-version/duplicate-key/nonfinite inputs, path escapes, no stale success and no unknown-field leakage. Fixtures are labelled TEST FIXTURE, not actual NASS observations.
- Targeted 45 tests and full 168-test regression passed. Full 168 tests also passed against the noneditable installed wheel in the second environment. Ruff passed. Both environments passed `pip check`.
- Built a wheel with the adapter/manifest, installed it noneditable in the second environment and confirmed imports in site-packages. Wheel inspection found packaged adapter/manifest and no restricted data/private outputs. The two runs on actual authorized aggregate artifacts produce identical complete bundles except their genuine UTC build timestamps. All three panels are available with the checked historical values. This did not rerun survey analysis or performance experiments.
- A tiny `AppTest.from_string` dependency smoke rendered a test metric successfully with Streamlit 1.66.1; this establishes that the selected testing SDK executes, not that any dashboard has been built or UI requirement verified. The expected bare-mode ScriptRunContext warning did not produce an AppTest exception.

The existing foundation CI now installs the M4 lock/extra and runs `pip check`, lint and synthetic tests; no additional workflow was created. Actual evidence inputs are not required for CI. A remote runner outcome must be observed separately.

## Reproduction and limitations

Commands are in [development setup](DEVELOPMENT.md). Actual bundle artifacts live only under ignored `reports/private`; the committed manifest contains checksums/provenance fields, not restricted rows. Manifest refresh requires a reviewed analytical snapshot, not automatic acceptance of whatever a browser supplies.

Hash agreement ensures byte identity with this reviewed snapshot. It does not establish scientific authenticity, permissions, representativeness or physical measurement accuracy. Aggregate arithmetic validation cannot recover raw order statistics or independently establish field identity. Scientific limits and benchmark exclusions remain mandatory reporting context.

Next implement Streamlit views, record formatting and selection-transition AppTest coverage under M4-03, then local startup/usability checks and M4 review under M4-04. No spatial filters, experimental reruns, raw-data uploads, public URL or automatic merging is introduced.

Learning checkpoint: an undefined precision has no predicted-positive denominator; it is not0% accuracy. A new build timestamp does not update the2022 survey period. A trusted checksum does not turn an unsupported population claim into a valid one.

Follow-up: [M4-03 UI verification](M4_UI_REVIEW.md) now records interface implementation and a local startup smoke check. The initial no-app statements below describe this earlier adapter checkpoint; browser/usability review remains pending.
