# M0-03 — Source feasibility review
Research date: 2026-10-26. **Metadata review only; no survey microdata were downloaded, inspected or ingested.**

## Candidate A — Nigeria National Agricultural Sample Survey (NASS) 2023
Official NBS catalog: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
World Bank metadata: https://microdata.worldbank.org/catalog/8194
FAO release: https://www.fao.org/in-action/agrisurvey/news/news-detail/the-national-bureau-of-statistics-of-nigeria-%28nbs%29-releases-nass-2023-report-and-microdata/en

- Designed as an agricultural household sample survey covering agriculture, crops, livestock and associated activities; **not a farmer registration census**.
- NBS metadata says anonymized 2024-07-31 v1.0; the FAO announced report/microdata availability on 2025-10-20.
- Sampling/weighting: multi-stage sampling with design/non-response adjustments; household observations cannot be summed naively into state or national estimates.
- Disclosure control: direct identifiers and specific addresses/GPS suppressed; below-LGA geographic detail removed in released microdata.
- Candidate purpose: defensible agricultural indicators with design-aware estimates after inspecting released variables, documentation, weights and access conditions.
- Caveat: a national data release does not ensure reliable precision for each Nasarawa LGA. Validate domains/sample sizes before LGA-level claims.

## Candidate B — Nigeria GHS Panel 2023–24
World Bank dataset metadata: https://datacatalog.worldbank.org/search/dataset/0066579/nigeria-general-household-survey-panel-2023-2024
NBS catalogue candidate: https://microdata.nigerianstat.gov.ng/index.php/catalog/82

- Nationally representative panel (~5,000 households), also designed to represent Nigeria's six geopolitical zones; post-planting and post-harvest waves.
- Research Data License stated by World Bank catalog. **Public metadata does not establish unconditional redistribution rights**.
- Candidate purpose: household socioeconomic/agricultural analyses in the appropriate supported domains; not a substitute for verified individual registries.
- Caveat: survey periods, sample designs, variable definitions and geography must be reconciled before cross-survey comparisons.

## Source due diligence checklist
- [x] Official catalog and study type verified from metadata.
- [x] Basic geographic, weighting and anonymization limitations noted.
- [ ] Download/access terms read and recorded for each individual file.
- [ ] DDI/data dictionary inspected for variables and identifiers.
- [ ] Dataset file hashes, download dates and versions recorded.
- [ ] Survey design variables (PSU, strata, weight), nonresponse and missing codes verified.
- [ ] Release/redistribution permissions explicitly checked.
- [ ] Proposed geographic aggregations vetted for sample adequacy/precision.
- [ ] At least two defensible analytical questions tested against variables.
- [ ] Source owner review and approval.

**Hard rule:** no raw survey data to be committed to GitHub without explicit redistribution permission and privacy review. A private repo does not waive usage restrictions.
