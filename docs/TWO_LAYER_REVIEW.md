# Two-layer presentation review

Date: 2026-10-30. The owner accepted the review distinguishing a stakeholder website from the technical evidence explorer and authorized implementation. **Both layers are now implemented within the existing Streamlit app.** This is a structural/content change, not another decorative-only refresh.

## Delivered experience

| Layer | Entry points | Purpose |
|---|---|---|
| Stakeholder | Overview, Agricultural insights, Engineering studies, About | Explain purpose, intended audience, findings and essential cautions with guided actions |
| Technical | Evidence & methods; existing Survey findings, Synthetic quality, Workload measurements | Inspect controls, definitions, counts/denominators, limitations and provenance |

Overview is the default, including after a fresh reload. It presents purpose, working calls to action and a survey-only summary: household records, plot records and crop participation with its valid-response denominator. It contains no technical selectors, raw fingerprints or synthetic totals. Topic cards lead to the other pages. Project purpose and intended usefulness are expressed without clients, deployment, national representativeness or business-impact claims.

Agricultural insights uses the verified participation response counts in a chart and explains missing plot-area sensitivity in plain language. Its coverage progress is known area values / total eligible plots, with both counts visible; an empty roster has no progress ratio. This is a record-completeness diagnostic, not a weighted population indicator. Sample/measurement limits and source/period remain beside each finding. Empty/undefined/unbounded states do not become zero-valued claims.

Engineering studies is explicitly separate and synthetic. Matching summary identifies Mixed/B1/duplicate-role/seed303, with precision and recall. Workload summary identifies the55000-event bounded-key local batch and preserves shared-machine/production limits. No common population or combined score is constructed. About explains the research/portfolio purpose and remains accessible if evidence loading fails.

Every evidence action is functional. Participation/area actions select the corresponding indicator; matching/workload actions reset stale controls to the exact summarized cell. Navigation persists only interface state. Both layers rebuild the same validated aggregate bundle on each interaction; no constants or cached-success data are introduced. A failed survey panel suppresses its overview/insight figures, while independently valid engineering views remain usable.

The [presentation contract](TWO_LAYER_PRESENTATION.md) was specified before implementation. Existing illustration/stylesheet resources are reused with no new image generation, dependency, frontend framework or hosting service.

## Verification

- Development full suite:223 passed in60.50 seconds. All36 existing explorer UI cases remain, covering both indicators,126 quality cells and12 workload/measurement choices.
- Eleven new stakeholder cases cover default entry, matching figure provenance, exact CTA destinations, stale-control reset, live invalidation, undefined participation, empty/unbounded/zero area states, independent engineering failures and About without inputs.
- Installed-wheel full suite:223 passed in27.08 seconds; pip check and isolated Ruff passed. Wheel SHA-256:3babc7c393c0e3e2f61ffa05aea12370f77371c1f04c06dd0b99958f6935ccb7. The new pages, UI, brand and asset bytes are checked against package resources.
- Final real-browser audit is ignored at reports/private/m4_browser_review/20261030T184814407831Z/review.json: Chrome156.0.8078.49,1440x1000 and390x844 CSS viewports,29 captures,12 checks passed, zero JavaScript exceptions, only127.0.0.1 observed tab request hosts. Both temporary ports closed with no cleanup notes.
- Browser checks include default stakeholder entry, actual packaged image decoding, native-keyboard CTA destinations, all preserved technical interactions, narrow drawer navigation, narrow stakeholder-to-evidence transition and no page-wide horizontal overflow. Selected final captures were separately inspected; visual_inspection.json records that scope.
- Exploratory failed audits are retained privately: one DevTools transport disconnect, an obsolete expectation that a reload opened the technical page, and an offscreen mobile drawer-close assumption. The driver now handles the new default route and scrolls the longer drawer before locating its native close control. No failed audit is reported as a completed browser pass.

Application model/SQL files, reviewed artifact bytes, manifest and dependency pins are unchanged. No new survey or benchmark experiment was run. No new remote CI result, multi-browser/physical-device, external-user or formal accessibility validation is claimed.

## Local handoff

The existing owner-requested local preview was restarted from the updated checkout at http://localhost:8501/. A separate real Chrome check against that exact port verifies the stakeholder overview and its technical-evidence action, with zero JavaScript exceptions. Its screenshots/check are ignored under reports/private/two_layer. Only the temporary verification browser was stopped; the local preview intentionally remains running. This is loopback-only, not a public deployment.

M4-06 closes this accepted two-layer increment. M6-04 release-readiness review remains open. Future navigation/framework expansion should follow demonstrated need rather than duplicating this analytics layer.

## Follow-up: stakeholder website redesign (2026-10-30)

The stakeholder layer now uses a website structure: top navigation, hero with actions, illustrated stat cards, a 100-square participation picture, a to-scale plot drawing, a checking-process band, inner-page banners and a footer with the image credit. Illustrations are drawn from validated bundle values by pure, unit-tested functions. A map slot shows abstract artwork only; boundaries and regional values stay excluded until the geography review in ADR-002 is decided. The technical explorer gained an in-page view switch, one source line per view and a back link. Evidence and limits are recorded in MEMORY.md (2026-10-30 stakeholder website redesign).

## Current website review and publication checkpoint (2026-10-30)

Owner requested inspection of the current website and pushing necessary updates. Reviewed the existing uncommitted M4-07 redesign rather than replacing it. Real Chrome confirms the top navigation, on-image actions, illustrated figures, inner-page banners and mobile layout. The map remains explicitly abstract with no boundaries or regional findings.

Corrected quantitative illustration edges before publication. The100-square picture now uses true nearest-integer rounding; a nonzero group smaller than a tile is stated explicitly with its exact percentage rather than inflated to a full square. Matching narrative uses fewer-than-one/more-than99 language near the endpoints. The square-area diagram expands its labelled reference above one hectare instead of clipping while claiming scale, rejects nonfinite values and explicitly describes an equivalent square rather than observed geometry. Median copy no longer makes an exact half-at-a-rounded-threshold assertion. Released-unit and sample limitations remain visible. The adapter change is only clearer seed-reference wording; indicator/SQL source, inputs, manifest and dependency pins are unchanged.

Full development248 tests passed in74.33 seconds; installed-wheel248 passed in45.63 seconds. Isolated Ruff and pip check passed. Final wheel SHA-256:59212f495e24bd5a7d76d0934753a6d52f7410172afebd14c70f61075fd53c20. Pure illustration tests cover tiny shares, invalid areas and reference scaling; existing navigation/availability tests remain active.

Final native browser audit: reports/private/m4_browser_review/20261030T211840543057Z/review.json,35 captures/13 checks passed, Chrome156.0.8078.49 at1440x1000 and390x844, zero JavaScript exceptions and only loopback tab request hosts. Both temporary ports closed with no cleanup notes. Selected narrow hero/navigation and area-story captures were inspected; desktop layout and live preview were also checked. The pure visuals module has a supplemental post-run source fingerprint. No new remote CI or formal accessibility/user-study claim is made.

The existing verified preview was restarted and separately checked at http://localhost:8501/: reviewed design and92.84% visible, zero JavaScript exceptions. It remains running locally; verification browsers are stopped. Private screenshots/logs/wheels remain ignored. M6-04 remains open; pushing reviewed code is not a hosted deployment or data redistribution.
