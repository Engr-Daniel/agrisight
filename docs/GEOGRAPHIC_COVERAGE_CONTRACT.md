# Geographic coverage contract GC1 v1.0

Specified before the new coverage aggregation. User request: assess and add map visuals where supported, without widening the website redesign.

## Question and interpretation

Where are the released household records represented? Show **recorded sample household counts by state/FCT**, not agricultural prevalence, national production, service need or targeting priority. No activity percentages, population estimates, ranks or confidence intervals by geographic domain are introduced. Unequal sample counts reflect the observed release and cannot establish differences in population agriculture. This narrow coverage question supersedes the earlier blanket map deferral only for this view; domain inference remains gated.

## Counting contract

Use the same frozen owner-authorized NASS archive as SA1. Read only complete unique household key and `state_id` from `1_households.dta`. Validate the released `STATE` label and all 37 state/FCT value labels; numeric codes are survey codes, never assumed to be alphabetic or ISO codes. Reject missing/unknown state codes, duplicate/missing household keys or unmatched boundary labels rather than dropping records. Python frequency counts and an independent SQLite GROUP BY must agree exactly. Sum of counts must equal the SA1 household input total. Do not expose household identifiers, LGA, enumeration-area identifiers or coordinates.

## Boundary and crosswalk review

Candidate: geoBoundaries gbOpen Nigeria ADM1, boundary ID NGA-ADM1-27671186, year represented2022, source GRID3; API metadata reports CC BY4.0. Inspect actual geometry and licence metadata before inclusion. Pin the supplied Git commit download URL and byte hashes. Explicitly review normalized name matches and the FCT alias; require a one-to-one match across all37 polygons and survey labels. No fuzzy matching. Preserve source attribution and disclose simplification. Use GeoJSON longitude/latitude with a documented display projection; do not infer distances, land area, cadastral accuracy or exact survey-boundary vintage equivalence.

## Disclosure and interface

Only state/FCT totals are exposed; no row-level or smaller geography drill-down. Suppress counts below30, including exact tooltips, tables and colour encodings; display no-data/suppressed categories distinctly. Do not offer filters that create smaller cells or reconstruct them through complementary totals. If any cells are suppressed, omit the total and all exact count tables for that map. This threshold is a conservative display rule, not proof of anonymity or unrestricted survey redistribution. Review observed minimum state size before enabling the actual map. Raw microdata and aggregate JSON remain ignored; no new release or deployment is authorized.

Display a responsive green choropleth and an accessible state/count table, with source, household grain, unweighted sample limitation, boundary attribution and meaning of colour. Geography is an optional independently validated component: unavailable geography must not hide nongeographic findings. Malformed, changed or unreconciled geometry/aggregates hide the map without fallback shapes or invented coordinates.

## Acceptance evidence

Manually counted fixtures, missing/duplicate/unknown keys and codes, boundary mismatch/hash failures, count reconciliation, suppression and unavailable-map states; actual SQL/Python equality; one-to-one37-state crosswalk; observed minimum cell size; installed-wheel reproduction; actual desktop/narrow browser chart/tooltips/layout checks. Record observed evidence separately, never complete this gate from a checklist alone.
