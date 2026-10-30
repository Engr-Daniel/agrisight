# M6-01 clean source reproduction protocol

Specified 2026-10-30 before execution. Scope: reproduce the committed source and synthetic/fixture checks on this Windows host in a new environment; this is independent of existing environments and working-tree inputs, not an independent person or operating system.

## Inputs and acceptance

1. Freeze the full Git commit; export only tracked files with `git archive --format=zip HEAD`. Extract into new ignored `reports/private/m6/<run>/checkout`. Record archive and lock SHA-256. Do not copy raw data, existing evidence aggregates, browser profiles or installed packages into that checkout.
2. Create a new Python 3.11 virtual environment without system site packages. Install the exported `requirements/m4.lock` (normal installer cache allowed), build a wheel from exported source with locked build tools and install it noneditable without dependency resolution. Require pip check and an exact distribution map matching the 45 lock pins plus agrisight0.0.1. Verify imports resolve to the new environment site-packages.
3. From the exported checkout run all tests and existing CI lint targets. Require 204 passed, no skipped reporting module; require lint success. Save commands, return codes and output privately. This is a local analogue, not an observed GitHub/Linux run.
4. Run synthetic KPI/quality examples and the reserved evaluation. Compare complete parsed evaluation JSON with the existing reviewed aggregate, including deterministic provenance. No survey data are needed. This rerun is a reproduction check, not a new reserved-seed experiment or baseline selection.
5. Run the adapter with no evidence inputs. Require exit1 and all three panels unavailable. No fallback values or real-data results may appear. Verify export contains only data/README.md and no evidence files.
6. Inspect wheel contents for required SQL/manifest/UI resources and excluded raw/private/environment files. Record actual results and limitations in a review; preserve failed logs and never mark a failed step complete.

## Boundaries and subsequent work

Do not rerun machine-dependent benchmark timings to claim byte equality. Existing measured performance retains its documented shared-machine and allocation limits. Actual survey regeneration requires an additional authorized-input lane with frozen archive hashes; fixture success cannot establish it. Browser review remains the M4 evidence, not rerun implicitly here.

Later M6 work must inspect actual remote CI, define/reproduce the authorized-data lane, and review software/data licences, privacy/disclosure, dependencies and secrets before any explicit owner-authorized public release or deployment. This protocol does not authorize publication or claim a comprehensive security scan.

## Provenance mismatch handling

If fresh execution reproduces metrics but differs in source/protocol hashes, retain both outputs and report the differing fields. Check whether raw source bytes differ only by CRLF/LF; a normalized diagnostic is not a substitute for the recorded raw-byte hash. Do not silently change the manifest, overwrite reviewed artifacts, or normalize historical hashes. A versioned line-ending/provenance policy and explicitly re-reviewed artifacts are required before claiming exact clean-source reproduction.
