# M0-05 — Official agricultural survey documentation audit
Reviewed: 2026-10-26. **Catalog-level review only; no individual data files downloaded.**

## NASS 2023 — National Agricultural Sample Survey
- Official NBS catalogue: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
- Study reference `NGA-NBS-NASS-2023-v01`; producer NBS; household sample survey, not a registry of all farmers.
- Reports agricultural household activities including crop farming, livestock, fisheries, forestry and labour.
- Survey reference year title: 2023; catalog also displays Nigeria 2022. Do not assume time reference for individual variables; inspect questionnaires/codebook.
- 767 of 774 LGAs were covered, excluding specified insecure LGAs; selected EA/household design. Geographic coverage **does not prove LGA-domain estimation precision**.
- Documentation in PDF, DDI/XML and JSON is linked on catalog page; it is **not yet inspected variable by variable**.
- No raw microdata retrieved; access and redistribution permissions remain pending.

## GHS Panel 2023–2024, Wave 5
- Official NBS catalogue: https://microdata.nigerianstat.gov.ng/index.php/catalog/82
- World Bank metadata: https://datacatalog.worldbank.org/search/dataset/0066579/nigeria-general-household-survey-panel-2023-2024
- Study reference `NGA_2023_GHSP-W5_v01_M`, edited anonymized release; units include households, individuals, agricultural plots, and communities.
- Approximately 5,000 panel households, designed for national and six-geopolitical-zone representativeness. Do not present LGA-level sample estimates as statistically reliable without design evidence.
- NBS catalog identifies restrictive access obligations: authorized copies only, no reidentification attempts, confidential handling of inadvertently identifiable material and source citation.
- World Bank catalog lists a **Research Data License**, not blanket approval to redistribute files.
- PDF/DDI/XML/JSON documentation links exist; variable-level and design weight audit is still outstanding.

## Proposed source workflow
1. Inspect documentation/weights for each source using official metadata and download controls.
2. Create data cards: study ID, provenance, file/version, release term, analysis grain, sample design, variable selection, weight and geography.
3. Request/acquire data only under permitted terms; do not commit restricted microdata.
4. Evaluate which specific indicators are measurable; no fabricated missing fields, farm GPS or LGA-level precision.
5. Keep official survey analysis separate from seeded synthetic registration data.

## Decision
NASS: **primary candidate** for agricultural descriptive analysis, conditional on variables, weights, permissions and geographic support. GHS: **secondary candidate** for household panel context. Neither serves as a real 55k farmer registry.

## Cautions
This document is a metadata study, not a codebook audit or evidence of downloaded datasets. The RFP context motivates the use cases but client-specific data/material are not part of AgriSight.
