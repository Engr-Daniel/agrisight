# M6-03 authorized survey reproduction protocol

Specified 2026-10-30 before execution. Freeze commit995b17719e285f23ec38b09bf32811487975e9b6; export from the repository root under both autocrlf settings and require identical file payloads and current working runtime bytes. Use the already isolated, pinned M6 environment with a noneditable wheel built from this export. Record its actual reused status, package path, dependency check and wheel hash.

Verify the owner-authorized ignored archive SHA-256 equals a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02 before reading it; use its absolute path without copying raw data into exported source. Run NASS-01/NASS-02 in both the working environment and installed-wheel export, writing new ignored paths. Require complete parsed JSON equality across those executions. Compare every non-provenance field with preserved historical outputs; independently computed SQL/Python reconciliation remains mandatory inside each model. If old provenance differs, enumerate it and preserve old bytes rather than silently re-signing.

Inspect actual GitHub run/job/step results and logs for the frozen commit, not a PR-only endpoint or inferred CI success. Record commit, run ID, runner/Python, test count and conclusion. Remote CI uses synthetic fixtures only; it does not verify actual microdata.

If survey outputs reproduce exactly and historical analytical fields match, explicitly review a new manifest snapshot selecting those outputs; preserve older snapshots and all active inputs first. Verify a complete actual bundle and installed-wheel resources/tests after any adapter/manifest changes. Historical workload measurements are not rerun/relabelled. Stop on unexpected numerical or source-hash differences; retain failed outputs/logs.

No new survey inference, measurement accuracy, geographic scope, source permission, public release authorization or benchmark claim follows from successful reproduction. Release licence/privacy/disclosure/security gates remain separate.
