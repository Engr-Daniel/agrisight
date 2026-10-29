# E2.1 — Main-season crop participation in the observed NASS sample

Observed: 2026-10-29. Indicator NASS-01 v1.0. **Unweighted released-sample description, not a national or domain population estimate.** This is the first M2 analytical workflow, not completion of AgriSight's broader agricultural research questions.

## Finding

**132859 of 143105 eligible recorded agricultural households (92.84%) reported growing crops during the main season, April–October 2022.** The remaining 10246 recorded households reported no for that question.

| Measure | Observed value |
|---|---:|
| Loaded household rows | 143105 |
| Numerator: crop participation yes | 132859 |
| Denominator: valid yes/no household records | 143105 |
| No responses | 10246 |
| Missing responses excluded | 0 |
| Other numeric responses excluded | 0 |
| Total response exclusions | 0 |
| Unrounded sample proportion | 0.9284022221445791 |
| Sample percentage, display rounded | 92.84% |

The denominator contains released agricultural-household observations, not every Nigerian household, distinct individual farmers, plot records or registrations. A no response means no main-season crop growing for this question; it does not imply no agricultural activity. The sample includes agricultural households selected by the survey's design, so this proportion must not be presented as Nigeria's household/farmer prevalence or as evidence of programme coverage.

## Method and provenance

Source: National Bureau of Statistics, Nigeria, National Agricultural Sample Survey (NASS 2023), owner-supplied anonymized archive acquired locally 2026-10-29. Archive SHA256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`; member `1_households.dta`. Exact upstream transaction and mirror byte identity are not independently certified. See [source/access card](../docs/data_sources/NASS_2023_CARD.md) and [inventory](../docs/data_sources/NASS_2023_INVENTORY.md).

Applied the pre-specified [NASS-01 contract](../docs/NASS_INDICATOR_CONTRACT.md) and [E2 protocol](../docs/experiments/E2_PROTOCOL.md). Required complete unique household keys, validated source reference strings and retained the raw archive unchanged. All loaded records qualified by key and yes/no response; no imputation, deletion, weighting or joins. Numeric 1 is yes, 2 is no. Other/missing responses would be excluded and reported; a zero denominator would yield null, not 0%.

The versioned [SQL model](../src/agrisight/sql/nass01.sql) creates constrained staging, a household eligibility view and a one-row indicator mart. Independent Python arithmetic directly aggregates selected source responses. Seven integer measures agree exactly; proportion and percentage agree within absolute tolerance 1e-12. Reader/normalization are shared and separately tested, not falsely claimed to be wholly independent source pipelines.

The source main-season string explicitly refers to April–October 2022 and is consistent with the reviewed methodology; the study title NASS 2023 does not make this a current observation. See [period/design review](../docs/data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md).

## What remains uncertain

No weights or confidence intervals are applied: usable household/plot variance-design information and estimator applicability remain unverified. This does not prove no suitable design information can be obtained. No claim of national representativeness, subnational precision, significance, causal effect, time trend, input/service access or actual irrigation use follows from this result.

Zero missing/invalid values on this field does not establish correct answers or full survey coverage. The E1 findings of missing areas/quantities and conflicting dry-season year remain relevant; none is repaired or analysed away here. Other activities can overlap, so counts of crop/livestock/fish participation cannot be added as distinct households.

## Reproduction and verification

From the repository root with the unchanged pinned E1 environment:

```powershell
.\.venv\Scripts\python.exe -m agrisight.nass01 data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/nass01.json
```

See [development setup](../docs/DEVELOPMENT.md) for full environment and packaged reproduction commands. Machine JSON includes source, definition, versions, SQL/code/lock hashes and reconciliation; it stays in ignored storage. This manually reviewed aggregate report is a private project artifact, not an external publication or transmission. Public release still requires owner authorization, source/disclosure review and fulfillment of citation/report-copy obligations.

## Next analytical step

Use this verified baseline to pre-specify E3 robustness questions and prioritize the survey-design evidence needed for more informative agricultural comparisons. One sample percentage is a first complete analytical workflow, not the final portfolio outcome. Do not add dashboards or database services merely to enlarge this result.
