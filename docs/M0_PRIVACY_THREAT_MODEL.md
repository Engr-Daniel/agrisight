# M0 — Threat model and geography gate
Status: baseline design; implementation verification occurs in later milestones.

## Assets / exposure
- **Synthetic operational profile:** risk of accidentally generating plausible identifying combinations and reusing them in a public demonstration.
- **Official survey microdata:** risk of redistribution outside data license, reidentification through small cells and location attributes.
- **Private repository or online dashboard:** risk of leaked credentials or unintended remote sharing.
- **Charts and maps:** risk of false precision, unsupported small-area estimates or exposing unusual combinations through filtering.
- **Audit trail:** risk of losing original observations or hiding correction/merge actions.

## Controls and acceptance tests
1. Synthetic persons have opaque IDs and no direct names, email, telephone or precise real addresses.
2. Public-demo datasets are synthetic/coarsened or expressly licensed statistical aggregates; user-visible provenance is unambiguous.
3. No data joins across survey/sample and synthetic populations for census-like totals.
4. Protect credentials in CI and config; no private secrets committed. Review dependencies and permissions before deployment.
5. Preserve raw synthetic submissions and log approved corrections/merges; never infer identity from name alone.
6. Do not plot actual respondent GPS points. Use licensed administrative polygons; verify polygon source, usage permission and CRS before GIS implementation.
7. Apply small-cell suppression and complementary disclosure checks **before** enabling granular geographic/commodity filter combinations. Threshold to be established with actual threat model and intended users, not invented now.
8. Validate denominator and missingness labels per chart, and prevent users inferring prevalence from selected survey samples without the correct design/weights.

## Required before M4 map release
- Approved boundary source with actual redistribution license.
- Verified level (state/LGA), CRS, join cardinality, coverage gaps.
- Test map joins and invalid locations; no invented lat/long.
- Data-source-specific disclosure policy and suppression tests.

All listed controls are *requirements*. They are **not yet evidence that a complete system enforces them**.
