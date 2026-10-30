# Provenance policy: agrisight-text-lf-v1

Specified 2026-10-30 before M6-02 regeneration. Tracked text uses UTF-8/LF, enforced by .gitattributes. Existing dependency locks and historical artifact_manifest_v1.json are explicit byte-preserving exceptions. Binary/raw inputs are never normalized. Git attributes stabilize text bytes; they do not make differing dependency/platform versions equivalent.

Continue hashing exact bytes, not silently normalized text. The synthetic evaluation now explicitly records provenance_policy=agrisight-text-lf-v1. This changes provenance metadata, not generator, detector, seed, metric or statistical definitions. Historical raw hashes and reports remain valid descriptions of their historical executions. No historical result is rewritten to claim it ran under this policy.

## Migration acceptance

Preserve all four current aggregate bytes privately and retain manifest snapshotv1. Normalize tracked text without semantic changes. Regenerate the synthetic reserved evaluation, require all run payloads identical to the preserved evaluation, and review the only changed top-level fields: provenance_policy, code_sha256 and protocol_sha256. Verify the lock hash remains identical. Execute tests/lint, build/install a wheel from a staged Git export with canonical bytes, and require complete synthetic JSON equality between working-source and exported installed-wheel runs.

Only after those checks, make a reviewed manifest snapshotv2 selecting the new evaluation. Keep all survey and workload entries exactly as snapshotv1: those remain explicitly historical and do not claim execution from current normalized source. Snapshot version is independent of unchanged manifest schema1.0. No automatic trust generator or uploaded manifest is added. Actual authorized-data regeneration and current survey source alignment remain M6-03.

The original evaluation stays privately archived with hashes; the active fixed-name aggregate can be replaced only after review, with prior/new hashes and reasons recorded. No timing results are edited, relabelled as new runs or required to reproduce byte-for-byte. Future source edits legitimately change raw hashes and require an explicit evidence review; LF stability is not a promise that all future outputs match.

## Git-byte clarification

The earlier audit measured a Git archive made under core.autocrlf=true: Git's export conversion produced CRLF even where repository blobs were LF. Direct git-show byte inspection distinguishes stored blobs from exported files. The policy therefore controls checkout/export conversion explicitly rather than assuming archive bytes always equal Git blob bytes.

The byte-preserving exceptions intentionally persist the historically observed CRLF lock/manifest bytes as Git blobs. Dependency version lines and historical manifest content are unchanged; their staged raw hashes now equal the original reviewed working hashes. Thus these files have a one-time storage-byte migration, not a dependency or evidence-content change. Their attributes recognize CR-at-EOL while retaining trailing-whitespace checks. Source/protocol text now exports LF regardless of core.autocrlf.
