# Stakeholder analytics phase 1

Observed local run: 2026-10-30. The [question and analysis contract](../docs/STAKEHOLDER_ANALYTICS_BRIEF.md) was written before this calculation. This is an internal analytical delivery, not a completed client engagement.

## What the data support

Source: owner-authorized NBS NASS 2023 archive, SHA256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`. All results below are **unweighted observed-sample summaries**, not national estimates. No confidence intervals or survey-design claims are made.

| Activity | Yes | No | Valid household denominator | Share | Period |
|---|---:|---:|---:|---:|---|
| Main-season crops | 132859 | 10246 | 143105 | 92.84% | April–October 2022 |
| Livestock / poultry | 99389 | 43716 | 143105 | 69.45% | 2022/2023 agricultural year |
| Fish farming / aquaculture | 3747 | 139358 | 143105 | 2.62% | 2022/2023 agricultural year |
| Fish capture | 6607 | 136498 | 143105 | 4.62% | 2022/2023 agricultural year |

Each activity has 143105 input household records and zero missing/invalid responses. The denominator is yes + no, not all people or all farmers in Nigeria. Households can report several activities, so activity counts cannot be added to obtain distinct households. Different reference windows prevent interpretation as a same-period activity ranking.

## Co-reporting, not simultaneous activity

Both crop and livestock responses are valid for all 143105 households; zero are excluded from this joint table.

| Main-season crops | Annual livestock | Households |
|---|---|---:|
| Yes | Yes | 91614 |
| Yes | No | 41245 |
| No | Yes | 7775 |
| No | No | 2471 |

The four mutually exclusive cells sum to 143105. Crop-yes cells sum to 132859; livestock-yes cells sum to 99389. This is a joint household calculation, not overlap inferred from marginal counts. The crop window is April–October 2022; the livestock window is the 2022/2023 agricultural year. Co-reporting alone does not establish integrated farming or causality.

## Plot composition and quality

| Main-season roster category | Plots |
|---|---:|
| Cultivated conventional plot | 258865 |
| Temporarily fallow conventional plot | 9806 |
| Kitchen garden / backyard | 5216 |
| Total | 273887 |

These are plot records, not households or cultivated acreage. Of all 273887 plots, 273839 have a recorded area and 48 do not. No missing area was backfilled. The released field is labelled square metres, but measurement lineage remains unresolved; missingness and measurement accuracy are different questions. This agrees with the prior NASS-02 roster and missing-area counts.

## Supported uses and exclusions

These findings support follow-up questions about multiple agricultural activities and data coverage. They do not establish service demand, production, income, intervention effects or budget priorities. The website makes those limits visible and directs recommendations back to the corresponding evidence.

Minor-season comparisons remain excluded because of the calendar conflict. Maps and geographical comparisons await identifier, boundary, survey-design and disclosure review. Group comparisons require a separately justified question and denominator; none were added merely to fill the interface. The GHS alternative remains deferred, without mixing surveys.

## Reproduce

Use the pinned M4 environment from the checkout root; the archive and resulting JSON stay ignored:

```powershell
.venv-m4/Scripts/python.exe -m agrisight.stakeholder_analysis data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/stakeholder_sa1.json
.venv-m4/Scripts/python.exe -m pytest -q
.venv-m4/Scripts/python.exe -m ruff check src tests scripts streamlit_app.py research_explorer_app.py
```

The calculation validates archive identity, released labels, periods, complete unique household/plot keys, parent relationships, allowed plot types and finite nonnegative areas. Independent Python and SQLite calculations reconcile activity counts, joint cells, plot types and area completeness exactly. The product adapter pins the reviewed aggregate bytes and provenance, checks accounting identities and cross-checks the historical NASS-01/NASS-02 artifacts. Synthetic experiment files are not required by the stakeholder website.

The source archive is not redistributed. M6-04 release-readiness and any new deployment remain separate gates. See the [implementation review](../docs/STAKEHOLDER_PHASE1_REVIEW.md) for actual validation evidence.
