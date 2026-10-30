# Activity explorer and sample-coverage map

Scope: focused Agricultural insights functionality and analytical presentation, not a whole-site redesign. The activity component is shared with Overview so its controls remain consistent.

## Behaviour and analytical meaning

All activities is the default. Four horizontal green bars use a common zero baseline and show exact formatted labels. The visual order is main-season crops, livestock/poultry, fish capture and fish farming/aquaculture. Percentages use each activity's valid yes/no denominator; count mode shows yes households on a common input-household scale. Missing/invalid responses are excluded from percentages, never converted to no. Undefined percentages are labelled and have no bar; zero remains zero.

A focused activity view places its visual next to percentage, yes household count, valid denominator, interpretation and yes/no/missing/invalid response breakdown. Switching units or returning to All activities does not change eligibility or underlying evidence. No new activity indicator or SA1 artifact was calculated. Periods remain on each bar and in the table: crops April–October2022, other activities the2022/2023 agricultural year. Overlapping responses and different windows preclude mutually exclusive or same-season interpretation.

The page proceeds from activities to crop–livestock co-reporting, plot composition and sample geography. Recommendations and other pages retain their scope. Browser review and tests are recorded below after execution.

## Map feasibility and decision

The owner explicitly requested map assessment and implementation. A narrow **sample-coverage** question is supported, unlike geographic population estimates. The [GC1 contract](GEOGRAPHIC_COVERAGE_CONTRACT.md) was written before aggregation. The household file has37 labelled state/FCT codes, all complete in the observed input. Exact labels were inspected; their order is not alphabetical or ISO order.

geoBoundaries metadata for [Nigeria ADM1](https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/) identifies boundary `NGA-ADM1-27671186`, represented year2022, source GRID3 and CC BY4.0. The actual simplified file was downloaded from its fixed Git commit URL and inspected:37 polygon features, CRS84 longitude/latitude. All names match one-to-one after case normalization and the explicit FCT alias. No fuzzy matching, centroids, household coordinates or LGA joins are used. Ring orientation is normalized for D3; upstream simplification and original coordinate precision are retained. The map uses Mercator for contextual display, not area/distance measurement or certification of exact survey-boundary equivalence. See [third-party notices](../THIRD_PARTY_NOTICES.md).

Independent Python and SQLite state counts agree and sum to143105, matching the reviewed SA1 household input total. Minimum state cell1536; maximum9043. The map colours observed sample record counts and tooltips show state and count. An accessible table contains the same37 aggregates. It does not encode crop prevalence, population totals, production, sampling probabilities or allocation priorities. No inference is made from unequal sample sizes.

Only aggregate state/FCT records are exposed. No household identifiers, identifying coordinates, EA or smaller geography enters the product. A count below30 causes all regional numeric counts and quantitative colouring to be withheld, including tooltips and table, to avoid complementary reconstruction. This conservative rule is not an anonymity guarantee or a new publication permission. Geographic missing/malformed/stale evidence hides only the map. All raw survey data and derived JSON remain ignored; only openly licensed public administrative geometry and its source metadata are packaged.

## Reproduction

The same pinned environment and owner-authorized archive are used. No dependency additions or public runtime map/tile fetches:

```powershell
# Download the public source URL recorded in THIRD_PARTY_NOTICES.md to ignored storage first.
.venv-m4/Scripts/python.exe scripts/prepare_nigeria_boundaries.py reports/private/geography/source.geojson src/agrisight/reporting/nigeria_adm1_source_metadata_v1.json src/agrisight/reporting/nigeria_adm1_v1.json
.venv-m4/Scripts/python.exe -m agrisight.geographic_coverage data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/geographic_gc1.json
.venv-m4/Scripts/python.exe -m pytest -q
.venv-m4/Scripts/python.exe -m ruff check src tests scripts streamlit_app.py research_explorer_app.py
```

The reviewed manifest pins aggregate bytes, source/model/contract/boundary provenance. The boundary resource retains upstream hashes and modification notes. A new output must be analytically reviewed before repinning; the commands do not authorize silently accepting changed inputs. The source filename is arbitrary; the fixed source URL and hash identify its bytes. Frozen public metadata allows geometry regeneration without relying on a changing API response.

## Verification

Observed validation:

- Targeted activity/product/geography suite:34 passed (19.76s initial;23.72s after legend and heading adjustments). New cases cover default comparison and both units, all focused selectors, return to All, response accounting, escaped labels, zero versus undefined, invalid household/state keys, geometry crosswalk mismatch, count/hash inconsistency, small-cell and complementary suppression, optional-map failure, accessible tables and all product navigation.
- Full suite:296 passed development97.84s and installed-wheel108.20s. Ruff and pip check passed in both environments. No new dependency.
- Actual GC1 Python/SQLite counts agree:37 state/FCT areas, total143105, minimum1536, maximum9043. All states are above the display threshold. Complete installed-wheel JSON reproduces byte-for-byte, SHA256 `993933955e66198033e2e5348e04725a1d66389e7c16d6e2924355a0a15700d7`. Source/model/contract/boundary hashes checked against current files.
- Public simplified upstream GeoJSON SHA256 `edd28050c7f1ae40471424605f74e4d2df83502e4f301089761ae18f8ae2fbbf`. Frozen source metadata and derived resource are packaged; source geometry is acquired separately and stays ignored. There is no runtime download of map tiles or boundaries.
- Initial actual Chrome desktop/narrow run completed with activity transitions, count/percentage values, state map and accessible table. Inspected desktop comparison, focused count, desktop map and narrow comparison/map captures. The narrow map's side legend reduced the usable map width; moved its legend below the geometry. Final browser/layout and packaging evidence follows below.

 External stakeholder validation, broader browser testing and M6-04 release-readiness remain open. Neither this local map nor a licence on public boundaries authorizes redistribution of the survey or deployment.

## Final verification record

- Final actual Chrome run `stakeholder-browser-20261030T225035Z`:16 checks passed across34 captures, desktop1440 x1000 and narrow390 x844; zero JavaScript exceptions; request hosts only127.0.0.1; no document/main horizontal overflow; both temporary ports closed; no cleanup notes. Keyboard transitions validate all four percentages, all four counts, focused fish capture in both units and return to All. The map and keyboard-openable state table render at both widths. Desktop and narrow hover checks independently show SOKOTO /4,590, matching the aggregate.
- Inspected final narrow map and tooltip captures: bottom legend leaves usable map width and the polygon tooltip is readable. Earlier inspected comparison and focused-view captures retain readable category labels, values, periods and interpretation. Screenshots/profiles stay ignored. An intermediate tooltip audit assumed a canvas renderer and failed; the helper was corrected to inspect the actual SVG state mark, then the complete final run passed. No application failure is inferred from that helper mistake.
- Final wheel SHA256 `0e14189a27920dc4adc73fa6a58785eb20816e9b4d176ee6ed1945ba766db391`; installed-wheel focused suite34 passed in26.88s after the final legend/copy changes. Prior full-suite296-pass results remain the regression evidence; no repeated full run is claimed for those presentation-only adjustments. Ruff and both pip checks passed.
- Refreshed the verified workspace preview on localhost8501 using a hidden, loopback-only server with telemetry off; health200 observed. It intentionally remains running. No public hosting, new deployment, survey redistribution or remote CI success is claimed by these local checks.
