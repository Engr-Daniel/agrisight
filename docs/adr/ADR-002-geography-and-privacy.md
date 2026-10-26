# ADR-002 — Geography and disclosure controls
**Decision status:** Proposed, pending owner approval (2026-10-26).

## Proposal
- Synthetic registration data: use explicitly fictional location assignments that can be grouped into realistic public administrative polygons, but never claim real farmer coordinates.
- Official survey data: honor released geographic resolution, suppression and complex-survey inference; **no fabricated coordinates, farms, household addresses or finer geography**.
- Aggregate geography is displayed separately per data origin.
- Map joins require independently checked boundary source, CRS, naming normalization and valid point/polygon behavior.
- Private development still follows least-data/least-access practice; before portfolio publication perform small-cell disclosure and filter-combination testing.
- Small-cell thresholds, role privacy and access rules are **undecided** until threats and stakeholder use are reviewed.

## Test ideas
Boundary mismatches, missing geographies, invalid lat/long, synthetic points outside permitted polygon, refused geolocation, multiple roles at one synthetic person, and filter-based re-identification attempts.

## Not decided
Which public administrative boundary source/license, whether LGA or state is the lowest safe display granularity, and whether any map points should be included in the public release.
