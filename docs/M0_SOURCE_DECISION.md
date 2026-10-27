# M0 source and sampling decision (2026-10-27)

## Decision
The first deliverable is a **fully synthetic, deterministic registry**. Official Nigerian surveys are a separate, optional evidence lane to be incorporated only after source-file due diligence during M1.

### NASS 2023
Official catalogue: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
This is a multi-stage agricultural household survey. The NBS metadata identifies household-listing weight `nasc_listing_weight` but this is **not by itself a verified final analysis weight for every variable**. Identify the appropriate household/crop/fishery weight, PSU/strata and survey design per statistic. While the survey covered 767 of 774 LGAs, survey coverage alone does not establish robust *LGA-level estimate precision*. Agricultural activities include crop production, livestock, fisheries and associated activities.

### GHS Panel Wave 5 (2023–2024)
Official NBS catalogue: https://microdata.nigerianstat.gov.ng/index.php/catalog/82
World Bank documentation: https://microdata.worldbank.org/catalog/6410
NBS questionnaire documentation includes post-planting/post-harvesting household, agriculture and community instruments. GHS Wave 5 collected household and plot data and is designed for national and geopolitical-zone representation, not arbitrary small-area profiling. World Bank metadata lists a Research Data License. Catalogues differ in release/version records (e.g. v01/v02); confirm actual release version **at download time**.

### Verification boundary
At this point **no individual codebook variables, microdata downloads, respondent GPS or file hashes have been verified**. NBS/World Bank source pages permit us to choose an appropriate analytical direction; they do not establish unrestricted redistribution.

## M1 source-file intake checklist
- [ ] Decide an actual research question and required variables.
- [ ] Record filename, catalogue ID, version/date, format, download terms and SHA256 checksum.
- [ ] Read questionnaires and machine variable labels/missing-value codes.
- [ ] Identify correct household/individual/plot grain, design strata, PSUs and weight fields.
- [ ] Specify estimand and justified geographic domain; suppress low-sample-size/unstable estimates.
- [ ] Respect Research Data License and publication restrictions; retain controlled local sources outside Git.
- [ ] Publish only genuinely permitted aggregate results with source and limitations.
