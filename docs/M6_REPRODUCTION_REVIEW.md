# M6-01 clean-source reproduction audit

Date: 2026-10-30. **Audit completed; exact historical provenance reproduction remains unresolved. M6 is in progress.** This is a fresh local environment/source export on the same Windows host, not a separate reviewer, Linux run or public release.

## Frozen inputs and method

The [protocol](M6_REPRODUCTION_PROTOCOL.md) was written before execution. Git commit `b472646436537820540b9269a668dac2209baeaa` was exported with `git archive --format=zip`, without working-tree inputs or existing environments. Archive SHA-256: `039cef36b77ffc4398e825ff35759457d76b381844139c7185a88e7e747a4045`. Exported M4 lock SHA-256: `645656b8389cc697e9497a086f50c202b24f7663b7800437ae7507e15cca03f2`.

A new Python 3.11.9 environment installed all 45 pins from PyPI using the ordinary installer cache. No installed packages were copied from another environment. The exported source was built with those build tools and installed as a noneditable wheel. Imports resolve to that environment's site-packages. No raw inputs, reviewed evidence files or personal browser profile were copied into the export. The only exported data file is data/README.md.

Private run directory: `reports/private/m6/20261030T075027Z/`. It retains identity.json, source.zip, install.log, per-command logs, steps.json, result.json, line_endings.json and the wheel. The inspection helper is private experiment orchestration, not an application dependency.

## Observed results

| Check | Result |
|---|---|
| Installed dependency map | Exact 45 lock pins plus agrisight0.0.1 |
| pip check | No broken requirements |
| Full tests, including reporting | 204 passed, no skips, 58.83 seconds |
| Existing CI lint targets | Passed |
| KPI and quality examples | Passed; valid/invalid fixtures behave as documented |
| Reserved synthetic evaluation | All run payloads match the prior reviewed aggregate exactly |
| Complete evaluation JSON | Differs in protocol_sha256 and code_sha256 only |
| Adapter without evidence | Expected exit1; survey, synthetic quality and workload all unavailable |
| Wheel inspection | Required SQL, manifest and UI present; no data/private/environment paths |

Wheel SHA-256: `900a0b251706247013a6cf45c86a8e210bb6ec04bbdb35b677c06c3d1f7d889c`. Wheel-byte equality with an earlier build is not an acceptance criterion; source bytes and packaging metadata can differ. No new benchmark or browser run was performed. These test timings are suite durations, not workload performance findings. No new remote CI/Linux outcome is asserted.

## Reproducibility issue found

The committed/exported synthetic_quality.py has 298 CRLF line endings; the working copy used by the historical evaluation has zero. The exported M3_04_PROTOCOL.md has 61 CRLF endings; its working copy has one. After diagnostic CRLF-to-LF replacement, each pair is identical. The E1 lock bytes match exactly. No source files were converted during the clean run.

Consequently, identical numerical results have different truthful raw-byte provenance hashes. Existing environment-to-environment checks shared working-tree bytes and did not detect this clean-source distinction. It is a provenance portability issue, not evidence of different synthetic metrics. It must not be hidden by treating normalized hashes as the original raw-byte hashes or re-signing the reporting manifest automatically.

## Repeat the check

Choose a new ignored run directory; do not reuse prior outputs as fresh evidence. From the repository root, export an explicit commit:

```powershell
$m6Run = Join-Path (Get-Location) 'reports/private/m6/NEW_RUN'
New-Item -ItemType Directory -Path $m6Run
# Use the full reviewed commit ID above to repeat this particular audit.
git archive --format=zip --output "$m6Run/source.zip" b472646436537820540b9269a668dac2209baeaa
Expand-Archive -LiteralPath "$m6Run/source.zip" -DestinationPath "$m6Run/checkout"
py -3.11 -m venv "$m6Run/env"
Set-Location "$m6Run/checkout"
& "$m6Run/env/Scripts/python.exe" -m pip install -r requirements/m4.lock
& "$m6Run/env/Scripts/python.exe" -m pip wheel --no-build-isolation --no-deps . --wheel-dir "$m6Run/wheels"
& "$m6Run/env/Scripts/python.exe" -m pip install --no-deps "$m6Run/wheels/agrisight-0.0.1-py3-none-any.whl"
& "$m6Run/env/Scripts/python.exe" -m pip check
& "$m6Run/env/Scripts/python.exe" -m pytest -q
& "$m6Run/env/Scripts/python.exe" -m ruff check src tests scripts/m4_browser_review.py streamlit_app.py
& "$m6Run/env/Scripts/python.exe" -m agrisight.kpi_fixture
& "$m6Run/env/Scripts/python.exe" -m agrisight.quality_baseline
& "$m6Run/env/Scripts/python.exe" -m agrisight.synthetic_quality --phase evaluation --output reports/private/m3_04_evaluation.json
& "$m6Run/env/Scripts/python.exe" -m agrisight.reporting_adapter --output reports/private/missing_bundle.json
# The final command must return 1; inspect all three unavailable panel states.
```

Follow the protocol for distribution/import/resource checks and complete JSON comparison. Stop on unexpected command failures; preserve logs. Do not copy the historical evaluation into the exported input directory to make the missing-evidence check pass.

## Next acceptance gate

M6-02 must define a versioned line-ending/provenance policy, preserve historical evidence, regenerate affected outputs from committed bytes and explicitly review any new manifest version. Then verify the authorized raw-data reproduction lane and actual remote CI, and complete licence/privacy/disclosure/dependency/secrets review. Public release or deployment still needs explicit owner authorization. None of these remaining gates is marked complete by fixture success.

## M6-02 clarification and follow-up

The original audit correctly observed different exported bytes, but direct Git-blob inspection later clarified the cause: core.autocrlf=true affected Git archive conversion. The repository source blobs themselves were LF. See the [policy](PROVENANCE_POLICY.md) and [migration review](M6_PROVENANCE_REVIEW.md) for the explicit export rules and resolved synthetic provenance lane. This audit remains historical evidence; survey clean reproduction and release gates remain open.
