# Grouped insights and contextual detail — 2026-10-31

The owner requested immediate reorganization and simpler communication of the
existing verified findings. This is presentation work: no source data,
calculations, analytical contracts, dependency pins or reviewed aggregate hashes
are changed. The product direction in PRODUCT_DIRECTION.md still governs.

## Information architecture

| Topic | Subjects |
|---|---|
| Activities | Four-activity explorer; expandable crop/livestock overlap and sample-coverage map |
| Crops & seeds | Crop portfolio/diversity; seed channels/combinations; input records |
| Water & land | Water management; tenure/travel; plot types |
| Harvest & markets | Harvest difficulties; sales/storage and broad loss reports |

Only the selected topic and subject are visible, reducing the former page's
continuous stack of charts. Existing selectors, count/percentage controls,
hover figures, exact tables and unavailable-evidence behavior remain available.
The source/sample qualification is stated once near the page heading:
“Unweighted survey sample; these are not national estimates.”

## Copy and context policy

- Lead with the question, visualization, observed finding and useful interpretation.
- Keep the counting unit, relevant denominator, exact reference period and source
  near each finding. Crops April–October2022 and annual activities2022/2023 remain
  distinct. Source year alone does not replace a reference period.
- Keep short interpretation essentials visible: activities/crops/source channels
  can overlap; no harvest is not automatically crop failure; missing quantity is
  not zero; storage and sales can coexist; infrastructure is not actual irrigation
  use or reliable water; the map is sample coverage.
- Put longer coverage, eligibility, measurement and inference explanations in
  “Understanding these figures” disclosures. Keep underlying exact tables.
- Data Quality now presents crop-portfolio coverage differences and input-quantity
  completeness alongside the existing activity and plot-area quality information.
  Crop charts identify their represented households instead of interrupting the
  chart with a coverage warning. Missing optional evidence hides its quality
  details, with no substituted numbers.
- Keep technical protocols and reproducibility evidence in the repository. The
  About page explains analytical scope without unnecessary client/field-enrolment
  disclaimers. Footer artwork credit is short and still identifies AI generation.

## Verification and limits

Updated UI assertions check the new copy and the location of coverage detail;
existing numerical/schema/security tests remain intact. New coverage checks
verify all groups/subjects, disclosures, fixture unavailable states and footer
copy. Actual desktop/narrow Chrome review exercises each subject, crop-mode
changes, travel, destination overlap and Data Quality coverage counts, and checks
horizontal overflow, runtime errors and owned-process cleanup. Final executed
results are recorded in MEMORY.md and TASK.md after completion.

Use `python scripts/grouped_browser_review.py` for the current navigation. The
older stakeholder browser CLI delegates to this current review; its older helper
functions remain historical support. Screenshots and browser profiles remain
ignored in reports/private. No new external deployment or remote-CI result is
claimed. Publication, survey design, seed-variety interpretation and quantity-unit
gates are unchanged.

Final verification:410 tests passed in development52.43s and installed wheel47.37s;
Ruff, diff and both dependency checks passed. The seven presentation modules in
wheel SHA256 `f857b8bf396f7ab1cd0862c372eb6c9c2f4ce4f824aa634ae8f786116cf9b70c`
match the checkout. Existing10 reviewed artifact hashes are unchanged.

Chrome156.0.8078.79 audit UTC `grouped-browser-20261031T052342Z`:20 checks and20
captures, desktop1440×1000 and narrow390×844;0 JavaScript exceptions; loopback
host only; no document/main overflow; both temporary ports closed. Crop disclosure
opens/closes and all eight subjects are reachable. Final narrow crop, desktop
activities and Data Quality captures were inspected. Workspace preview8501 was
restarted hidden after command-line verification, health200 observed; it remains
running. Browser screenshots/profiles remain private. No recalculation or new
deployment was performed.
