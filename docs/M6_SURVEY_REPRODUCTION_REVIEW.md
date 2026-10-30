# M6-03 authorized survey reproduction and CI review

Date: 2026-10-30. **Complete for current-source NASS-01/NASS-02 reproduction on the tested Windows environment and observed remote fixture CI.** Release-readiness review remains open.

## Frozen inputs and execution

The [protocol](M6_SURVEY_REPRODUCTION_PROTOCOL.md) was specified before execution. Exported commit `995b17719e285f23ec38b09bf32811487975e9b6` from the repository root with autocrlf=true/false; file payloads are identical and match working bytes. Source ZIP SHA-256: `3aad914d8e92efe6b12ef5a7037e4b7bc02d5c869c6130f26fc7cfd94b2f1556`.

The authorized local archive is118711951 bytes and matches frozen SHA-256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02` before reading. It was referenced by absolute local path and not copied into exported source, Git or CI. Output consists of aggregates only; no respondent records were published.

Built the committed export and installed its wheel noneditable into the existing isolated M6-01 pinned environment, rather than claiming a new environment. Pip check passed. Wheel SHA-256: `8156c4f3155b94a3e55c189e022bc0bb4db5a7e29c24b4ebb012ced037091d65`. Packaged NASS Python, SQL and active manifest bytes match the working files. Both indicator modules ran separately in the working environment and exported installed-wheel checkout, using Windows Python3.11.9 and the pinned dependencies.

Private evidence: `reports/private/m6_03/20261030T133150Z/` contains identity.json, frozen source archives, preserved historical aggregates, command logs/steps, result.json, CI observation and wheel. Fresh working outputs are ignored under reports/private/m6_03; exported outputs are beneath that checkout's ignored reports/private.

## Observed survey results

| Indicator | Reproduced finding | Output raw SHA-256 |
|---|---|---|
| NASS-01 |132859 yes /143105 valid households;92.84022221445791% |55524d5313a9f0148a92f8fb9c9a83af05e48a479025bdddbea2232f33410f3e |
| NASS-02 |273887 plots;273839 known areas;48 missing; median lower=upper6070.290058851242 in released labelled square metres |222d33cce613787ee7d61c0bc1164b32c6d42c6aa7423142d391afdc3929c9a4 |

Complete parsed JSON matches between working-source and installed-wheel executions and historical results. Raw artifact hashes also match historical bytes: no numerical, definition or provenance differences. Both model executions include their independent Python/SQL reconciliation and existing input/period/key/label guards. This was a reproduction, not a new empirical finding.

With the newly generated survey outputs and byte-identical copies of the reviewed synthetic inputs, the installed adapter verifies all four artifacts and makes all three panels available. All active original input bytes are unchanged. **Manifest v2 remains valid; no replacement or re-signing was necessary.** Historical workload timings were not rerun or relabelled.

The unchanged research limits remain: pooled unweighted sample, no national/domain confidence intervals; unverified area measurement lineage; missing-area bounds are not measurement-error bounds. Reproduction establishes implementation consistency, not source accuracy, representativeness or new redistribution permission.

## Actual GitHub CI

Observed [Foundation CI run41058930403](https://github.com/Engr-Daniel/agrisight/actions/runs/41058930403), push event for the frozen commit above, completed successfully on2026-10-30. Job124073425882 and its install/lint/test steps all succeeded. Downloaded job logs show Ubuntu24.04, Python3.11.17, no broken requirements, Ruff success and **209 passed in8.87 seconds**.

This is actual remote Linux fixture-test evidence, not an inference from local success. GitHub CI receives no authorized survey archive; it does not reproduce survey outputs on Linux. Windows tests from M6-02 remain209 passed in development/installed-wheel environments. No new local full-suite run was needed here because application/test/dependency/manifest bytes are unchanged; the new verification consists of real-data reruns, package/bundle checks and CI inspection. Test-suite elapsed time is not workload performance.

## Visibility and handoff

The repository API currently reports public visibility, independently confirmed on2026-10-30. README's former private label is corrected. No repository visibility was changed by this work. Public repository metadata does not establish that source-data redistribution, a package release or hosted deployment has been reviewed or authorized.

M6-03 is complete. Next is a concrete release-readiness audit: review software/data permission scope, tracked/history disclosure, secrets/dependency exposure and deployment threat boundaries; record unresolved items and obtain explicit owner authorization for any new release or deployment. No release/deployment action is included here. M5 remains optional. No server was started.
