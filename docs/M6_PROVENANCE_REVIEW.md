# M6-02 provenance migration review

Date: 2026-10-30. **Complete for the synthetic reproduction lane and explicit Git-byte policy.** M6 remains open for authorized-data clean reproduction, actual remote CI and release review.

## Decision and cause

[agrisight-text-lf-v1](PROVENANCE_POLICY.md) keeps exact raw-byte SHA-256 semantics and makes tracked text LF through .gitattributes. No normalizing hash function hides byte differences. Direct Git-blob checks clarified the M6-01 diagnosis: source blobs were LF, while Git archive under core.autocrlf=true produced CRLF. Explicit attributes now stabilize exports with autocrlf true and false.

Two dependency locks and historical manifest v1 retain the exact CRLF bytes observed in the reviewed working environment. Their Git blobs make a one-time LF-to-CRLF storage migration under -text; version lines/manifest values are unchanged, and their original reviewed raw hashes are preserved. This is a storage-policy change, not a dependency update. Git whitespace attributes allow CR-at-EOL while retaining other whitespace checks. Other text's working-tree normalization changes no analytical definitions.

Synthetic evaluation now records provenance_policy=agrisight-text-lf-v1. Its generator/contract version stays1.0 because generation, detection and metrics are unchanged. The policy identifies a provenance-format addition, not an improved accuracy claim or new held-out experiment.

## Evidence migration

Before regeneration, all four active aggregate files and manifest v1 were copied into ignored `reports/private/m6_02/20261030T124746Z/`, with historical hashes recorded. No raw rows were written or added to Git. Historical Git commits/reports are retained.

| Evaluation artifact | Raw SHA-256 |
|---|---|
| Historical | a45eafe5e95ed12aa83a74bc1e6be336779aa7ab0231d12bba8ee7ec789929b2 |
| Regenerated | a0cac276dc427decfbd931bc583139e827c5320744c39a533592a0009ddb2189 |

All run payloads match exactly, including observation/truth hashes, counts, accuracy and scenario breakdowns. Only code_sha256, protocol_sha256 and the added provenance_policy differ at top level. The lock hash remains unchanged. The active fixed-name synthetic aggregate was replaced after that comparison; the original bytes remain archived.

The adapter now loads packaged [manifest snapshot v2](../src/agrisight/reporting/artifact_manifest_v2.json), with snapshot_revision2 and unchanged manifest schema1.0. Only the synthetic quality entry changes; it requires the new policy as well as exact reviewed artifact/provenance hashes. Survey and workload entries are identical to [snapshot v1](../src/agrisight/reporting/artifact_manifest_v1.json). Those are explicitly historical inputs, not reruns from normalized source. Updating the manifest observation date means reinspection on2026-10-30, not a new survey vintage or benchmark measurement. The browser audit helper now fingerprints the active snapshot.

## Verification

- Development: all209 tests passed in53.12 seconds; isolated Ruff passed; actual adapter returned all three panels available.
- Five new regression cases check exact source/protocol/lock byte hashes, CRLF/LF distinction, correct/missing/wrong policy behavior and preserved historical manifest entries. A bad policy blocks only quality, preserving unrelated valid panels.
- Staged Git tree `a0bee9adb53b167ce28f3631dbbf1c8e064c04e5` was exported under autocrlf=true and false. All102 exported file payloads are identical between settings and equal their working bytes, including the frozen exceptions. Documentation additions after this tree do not change tested runtime/resource bytes.
- Built and installed the exported source as a noneditable wheel in the previously fresh M6-01 pinned environment; this environment was reused, not newly created. Pip check and Ruff passed; all209 installed-wheel tests passed in45.08 seconds.
- The installed wheel regenerated synthetic evaluation JSON identical in every field to the active working-source result. With copies of the three historical reviewed inputs, complete reporting bundles match except genuine build UTC timestamps; all panels are available.
- All historical archived hashes and unchanged active survey/benchmark bytes were verified. Packaged v1/v2 manifests and synthetic source bytes match the exported files. Wheel SHA-256: `9418f191c38a88106803fc702bd9f305c86db9d675113145ba31969d33d76f1d`.

Private evidence includes regeneration_review.json, normalized_files.json, steps.json, per-command logs, both archives and result.json in the run directory above. An initial audit-driver attempt used the reports subdirectory as cwd and therefore exported only that subtree; it was rejected before package execution. Its archives are retained with failed_subdirectory prefixes. Corrected repository-root exports establish the results above.

## Repeat and remaining gates

Follow the [clean reproduction protocol](M6_REPRODUCTION_PROTOCOL.md) using the current commit and include .gitattributes. Export from the repository root; explicitly compare file payloads using `git -c core.autocrlf=true archive` and `git -c core.autocrlf=false archive`. Build/install with the unchanged pinned environment, run tests/lint and evaluation, then compare complete parsed JSON. Keep private historical evidence separate from regenerated outputs. No new dependency, framework, raw-data access, browser run or timing benchmark was introduced here.

The synthetic lane now reproduces exact provenance across the two tested Git settings on Windows. This does not establish another operating system/Python version, authenticity of external data, authorized survey reproduction, remote CI, comprehensive security scanning or release permission. M6-03 must verify current-source survey outputs using the frozen authorized archive and inspect actual remote CI. Scientific limitations, licence/privacy/disclosure review and explicit owner approval for eventual publication/deployment remain active.
