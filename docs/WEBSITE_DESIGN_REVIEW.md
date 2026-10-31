# Professional agricultural website design — 2026-10-31

The owner requested the professional website design phase: visual hierarchy,
consistent typography, agricultural brand identity, purposeful imagery (farmers,
land, irrigation, fish, crops, seed, livestock, ponds), a moving Overview hero,
appropriate charts, responsive layouts and better navigation, **without reopening
the analytical work**. No model, SQL, contract, aggregate, manifest, dependency
pin or reviewed artifact changed; every number on the site still comes from the
existing verified bundles.

## Design decisions

| Area | Decision | Why |
|---|---|---|
| Imagery | Twelve original vector scenes (`site_art.py`): crop field, livestock, fish pond, canoe fishing, irrigation, seeds, inputs, land and travel, kitchen garden, harvest, market, survey interview | One coherent style; no licence or attribution risk; offline and fast (deterministic SVG); obviously artwork, so never mistaken for surveyed people or places. Scenes contain no numbers (tested). |
| Hero | CSS-only crossfading slideshow of six activities with captions and progress dots; paused and reduced to one slide under `prefers-reduced-motion` | Moving storytelling without JavaScript (Streamlit strips scripts); accessible motion. |
| AI photograph | No longer used on the stakeholder site; still used by the research explorer | Mixing a photoreal AI image with illustrations was stylistically inconsistent and needed an AI-generation credit. The footer now says "Illustrations are original AgriSight artwork." |
| Navigation | Nine subjects as one row of wrapping chips (`st.pills`) under an illustrated subject banner; the topic is a label on the banner | Replaces nested tabs, which overflowed on phones ("Harvest & mark›"). All subjects visible at once; one tap. Overview topic cards deep-link to subjects. The selected subject survives visits to other pages. |
| Overview | Story order: hero → source → key figures → illustrated activity cards → crop × livestock mosaic → topic grid → how to read | Question → evidence → implication. The activity explorer moved to Insights to avoid duplication. |
| Charts | New area-true mosaic for crop × livestock co-reporting (widths = crop answer, heights = livestock answer, legend with exact counts); existing reviewed charts kept | The overlap was table-only. A mosaic shows part-to-whole for two binary answers honestly. |
| Tables | `brand.table` adds locale thousands separators to integer columns; yes/no capitalised | Cards said 132,859 while tables said 91614. Underlying values unchanged. |
| Type and colour | Georgia display headings over the app sans; forest/leaf/wheat/cream palette; 4 px spacing base; 18 px card radius | Consistent hierarchy and agricultural identity without web-font requests (loopback-only policy). |

## Copy assessed individually

Changed: the source line now reads "Figures count surveyed households and plots
without survey weights; these are not national estimates" (was "Unweighted survey
sample…"); "Understanding the analytical scope" became "What these figures can and
cannot tell you"; banner leads use plain questions. The third recommendation now
leads with the undocumented area-measurement method and mentions the 48 missing
values second. Fixed encoding damage in the Water Management footnote (`?` → `·`/`–`).

Kept deliberately (needed for correct reading): valid responses, denominator,
reference period, counting unit (households/plots/records), "not national
estimates", co-reporting caveat, missing ≠ zero. Module-level reviewed copy inside
each subject is unchanged; candidates for later plain-language review include
"eligible records", "expected skips", "complete-vector denominator" and
"recorded branch".

## Verification

- `pytest`: 432 passed (410 before; 22 new tests in `tests/test_website.py` and
  `tests/test_grouped_presentation.py` cover valid scene SVG/alt text/no numbers,
  mosaic area accuracy, empty and undefined cases, escaping, reduced motion, chips,
  deselection, page round-trip, deep links and Overview values from the bundle).
  Existing UI tests changed only their navigation step (open Insights, choose a chip);
  assertions are unchanged.
- Ruff passed for src, tests, scripts and both launchers. A locally built wheel
  contains `site_art.py`, `website.py` and `assets/website.css`.
- Chrome 156 `scripts/grouped_browser_review.py`, run
  `grouped-browser-20261031T061942Z`: 22 checks, 22 captures at 1440×1000 and
  390×844, 0 JavaScript exceptions, loopback requests only, no page overflow, both
  temporary ports closed. Chips are selected with real pointer events; the topic
  deep link is exercised.
- Computed WCAG contrast: all text pairs ≥ 5.0:1 (AA). Coloured mosaic blocks
  ≥ 3.6:1 on the card; "Neither" is a labelled pale neutral, and exact values are in
  the legend and alt text.
- Desktop and phone screenshots of every page and subject were inspected.

## Follow-up after external review (same day)

An external review of commit `09db02c` (CI `smoke` success observed via the GitHub
API) recommended three changes before merging:

1. **Chart values visible without hover.** Bar values are now always shown; the
   secondary detail line (counts and period) still appears on hover, focus or tap.
   This supersedes the hover-only rule in CHART_HOVER_REVIEW.md. A CSS regression test
   ensures values are never hidden, and the browser review checks they are visible
   without hovering at both widths.
2. **Keyboard use of the subject chips, checked with real key events in Chrome.**
   Tab reaches the chip group (5 presses from the page start). The arrow keys move
   focus between chips without selecting (toolbar pattern), and Space or Enter
   selects. Focus stays on the chip after the rerun, with a solid gold focus ring.
   The earlier failure came from focusing the chip by script, not from the widget.
   The browser review now exercises Tab → ArrowRight → Space at both widths.
   A screen-reader pass is still not done.
3. **Artwork density.** Subject pages use a compact banner (shorter, smaller
   heading) so the chart reaches the first desktop screen. Full banners remain on
   Data quality, Recommendations and About.

Verification: 433 tests pass; Ruff clean; Chrome run
`grouped-browser-20261031T070717Z`: 26 checks, 22 captures, 0 JavaScript exceptions,
loopback only, ports closed.

## Limits and open items

- Keyboard selection is verified in Chrome (see follow-up); a screen-reader check
  (NVDA/VoiceOver) of the chip group's announcements is still open.
- While a subject is loading, Streamlit briefly dims elements from the previous page,
  so one screenshot captured a faded button mid-transition. It is not present once
  the run completes.
- Illustrations are generic artwork. Real photography would need licence-verified
  sources or the owner's own photos, and consent for identifiable people.
- No deployment, external hosting or remote-CI result is claimed. M6-04 release
  review remains open.
