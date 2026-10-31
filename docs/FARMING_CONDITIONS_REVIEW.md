# FC1 delivery review — 2026-10-31

## Scope and decisions

The owner requested all four remaining stakeholder questions in one run and
asked for visuals appropriate to each question. Read project state, prior
opportunity review, existing models/adapters/UI/tests, released metadata and
questionnaire pp13,20–30,39 before implementation. The versioned
[contract](FARMING_CONDITIONS_CONTRACT.md) preceded new calculations.

The four sections share one reproducible aggregate and one optional trust
boundary, while retaining their distinct grains and eligibility rules:

- Land: plot tenure/transport and travel bands; on-dwelling travel is a skip.
- Difficulties: separately recorded temporary non-vegetable/vegetable response
  branches; no-harvest reasons and incomplete-harvest shock questions.
- Destinations: harvested household–crop sales, storage, broad loss reports and
  paired sales/storage overlap, with no plot-level destination join.
- Inputs: recorded household–input types and quantity status, not total amounts
  or household adoption rates.

No explicit reliable vegetable flag was found in the selected schema. Assignment
therefore follows exclusive recorded harvest-response branches, with both/neither
branches audited. Actual data have zero unassigned/ambiguous temporary records;
the fixtures exercise both cases. Missing eligible shock responses remain
missing. Input questionnaire units and stage-specific loss quantity/percentage
alternatives prevent credible amount comparisons; those extensions remain gated.

## Implementation

`farming_conditions.py` validates required schema, stable source keys, household
and plot parents, temporary crop references, category/type codes and archived
periods. SQLite sees numeric raw responses, not precomputed Python category
counts. Category queries, subset sizes, quantity statuses and complete-response
overlap must match independent Python calculations. Read-only published summaries
contain no respondent IDs, coordinates or raw quantities. Executable SQL views
and bounded indexes are packaged; there is no new application dependency.

`conditions_reporting.py` verifies the private artifact hash and expected
provenance, then checks accounting identities, category labels, branch counts,
paired-response marginals and per-crop totals. It creates a fresh allow-listed
projection. Source origin and core household/plot totals must match; fixtures
cannot silently mix with real evidence. Missing/altered evidence hides only the
optional section. Crop detail requires at least30 field-valid responses.

`conditions_presentation.py` supplies four tabs within Agricultural Insights:
tenure ring, ordered travel/transport dots, harvest/reason dots, paired crop
sales/storage dots, sales/storage overlap matrix and input completeness matrix.
Dot charts switch percentages/counts; ring/matrices retain composition scales.
All mark values use hover tooltips; tables and analytical context remain visible.
No time-series chart or additional geographic prevalence map is introduced.

## Verification record

Executed targeted tests covering manually counted positive, negative and edge
cases: ownership versus free use, on-dwelling/unknown transport, fractional codes,
branch ambiguity, expected skips, missing shock responses, multiple reasons,
field-specific denominators, complete-response overlap, positive/zero/missing/
invalid quantities, tagged missing, duplicate/orphan keys, altered SQL, small
crop-detail thresholds, hash tampering, fixture origin mismatches, empty data and
UI selector/unit transitions. The final targeted30 tests passed in9.98 seconds.
An earlier full development regression run passed406 tests in89.71 seconds;
final regression/package/browser results follow in MEMORY.md after execution.

Commands used include `python -m agrisight.farming_conditions ... --output
reports/private/farming_conditions_fc1.json`, `python -m pytest -q`, `python -m
ruff check src tests scripts`, offline `pip wheel --no-build-isolation --no-deps`,
installed-wheel analytical reproduction and `scripts/stakeholder_browser_review.py
--fc-only`. Logs/screenshots/artifacts stay under ignored `reports/private`.

All four prior survey/engineering artifacts and SA1, IR1, CP1, SS1 were checked
against their existing manifest hashes and are unchanged. Complete final JSON,
packaged source and resource hashes must agree before marking the TASK items
done. Browser review must exercise all four tabs and controls at1440×1000 and
390×844, actual rendered marks/tooltips, layout overflow and process cleanup.

## Findings and limits

[Observed findings](../reports/FARMING_CONDITIONS_FINDINGS.md) explain what each
count can support and questions stakeholders can investigate. No national
prevalence, confidence interval, weather causation, current-condition, yield,
profit, legal-title, adequate-storage, input-access or adoption claim is made.
Raw data are never committed; existing archive permissions are not expanded.
This increment is local analysis/presentation, not a deployment or completed
privacy/licence/disclosure release review. M6-04 and seed variety/certification
interpretation remain open.

## Final observed evidence

Final development409 tests passed63.48 seconds; final noneditable installed-wheel
409 passed51.88 seconds. Targeted31 passed17.36 seconds after the LF guard;
Ruff and both dependency checks passed. Final wheel SHA256
`fad90c1b988130ab288ea52e8f931203b104c60f761d25367f9196adf8922ce1`.
Packaged model, adapter, presentation, SQL, metadata and manifest bytes match the
checkout. No application dependency change.

Canonical LF complete aggregate SHA256
`65275b5b590d76ee194d631cff4b44da99480a895c501839165bab728cf0b1ff`
reproduces byte-for-byte in development and installed-package calculations.
Current model/SQL/label/contract/lock hashes were checked before pinning the final
manifest. Initial generated metadata used Windows newlines; normalizing new
packaged JSON and explicitly emitting LF required fresh analytical runs in both
environments. Results are unchanged; no new Linux execution is claimed.

Actual Chrome156.0.8078.79 review UTC `stakeholder-browser-20261031T045153Z`:
18 checks,20 captures,1440×1000 and390×844,0 JavaScript exceptions, loopback-only
request host, no document/main horizontal overflow, both temporary ports closed.
Visited all four topics, both harvest branches and their four questions, land
views, crop detail, overlap and broad losses, and unit transitions. Native input
tooltips expose status/count/denominator; the rendered grid has84 cells in21
distinct rows. Reviewed final desktop input matrix and narrow overlap plus
desktop/narrow tenure, travel and destination captures. The first shortened input
labels collided on “Other”; separate organic/pesticide labels and a regression
test now preserve all21 input types. The tenure ring was resized after inspecting
legend clipping. Browser helper selectors/waits were adapted to actual React Aria
tabs and dependent control rendering. Screenshots remain private.

Final pinned evidence was subsequently checked in the real application: four
tabs render without exceptions or evidence-unavailable messages. Verified
workspace preview8501 was restarted hidden with telemetry off and returned
health200; it remains running. Document links/diff checks passed. Prior four core
artifacts and SA1/GC1/IR1/CP1/SS1 hashes remain unchanged. No remote-CI execution,
deployment, new data permission or completed release review is claimed.
