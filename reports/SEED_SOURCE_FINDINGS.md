# Seed sources SS1

Observed2026-10-31. [Contract v1.1](../docs/SEED_SOURCE_CONTRACT.md) defines the temporary household–crop universe, binary codes, overlap, combinations and variety gate. Source: frozen owner-authorized NBS NASS2023 archive. Results are unweighted observed-record descriptions, not national estimates or percentages of unique farmers.

## Grain, period and coverage

| Measure | Count |
|---|---:|
| Household records checked | 143105 |
| Seed household–crop records checked | 414049 |
| Eligible temporary household–crop records | 349068 |
| Excluded permanent/continuous records | 64981 |
| Households represented by eligible records | 119897 |
| Crop-yes households without an eligible seed record | 12962 |
| Represented households lacking crop-yes response | 0 |

The eligible records carry exactly `2022/2023 RAINY SEASON (APRIL 2022-OCT 2022)`; excluded permanent records carry `2022/2023 AGRICULTURAL SEASON`. Period/type pairings, complete unique household–crop keys, parent households, exact source/crop labels and0=No/1=Yes labels are validated. Seed and crop-portfolio rosters are not assumed identical. A household can contribute several crop records;12962 absent temporary-seed records at household level do not automatically mean non-use, missing interviews or permanent-only farming.

## Reported channels

| Source | Yes records | No records | Valid response denominator | Missing | Share |
|---|---:|---:|---:|---:|---:|
| Produced on the holding | 219313 | 129733 | 349046 | 22 | 62.83% |
| Community exchange | 12548 | 336498 | 349046 | 22 | 3.59% |
| Purchased from local market | 146869 | 202177 | 349046 | 22 | 42.08% |
| Purchased from seed company | 10384 | 338662 | 349046 | 22 | 2.97% |
| Received as a donation | 5239 | 343807 | 349046 | 22 | 1.50% |

Each field has349068 eligible records,349046 valid binary responses,22 missing and0 invalid. Share=yes/(yes+no). Missing is not coded as no. Channels can overlap; shares cannot be added to count unique households or total seed volume. A record-level source share is not a farmer adoption rate or proof of source availability/affordability.

Seed produced on the holding is the most frequently selected recorded channel by yes count; local-market purchases also appear frequently. This supports follow-up about how households obtain seeds for their recorded crops. It does not establish seed quality, resilience, unmet commercial demand, modern/improved adoption, certification, suitability or the effects of a programme.

## Exact source profiles and published grouping

Combinations use349046 complete five-response vectors;22 incomplete vectors are excluded. Independent Python and SQLite groupings agree on the exact private masks. The product publishes up to six frequent exact profiles and pools every remaining profile, so no individual rare mask/count pair is exposed.

| Published profile | Records | Share of complete vectors |
|---|---:|---:|
| Holding production only | 183079 | 52.45% |
| Local-market purchase only | 110515 | 31.66% |
| Holding production + local market only | 29056 | 8.32% |
| Seed-company purchase only | 6201 | 1.78% |
| Community exchange only | 6193 | 1.77% |
| Donation only | 2248 | 0.64% |
| All other observed profiles, pooled | 11754 | 3.37% |

These groups sum to349046 and are mutually exclusive, unlike the overlapping source marginals. A52.45% holding-only profile and62.83% holding-source share are different measures with the same valid universe. The top-six displayed chart can include the pooled residual when sorted; the complete published table retains every published group. Rounded shares need not sum to exactly100%.

No all-zero vector occurs in this actual eligible complete subset. The model nevertheless supports it as “No source selected,” not proof that no seeds were used. Very small private combination counts motivated the documented contract presentation amendment: at most six named profiles of at least30 records and a pooled residual; a small nonzero residual or complete universe below30 withholds the quantitative combination view. These are conservative display rules, not proof of anonymity or completed release approval. There is no geographic/crop filter or identifying row drill-down.

## Why variety percentages are withheld

The [NBS released modern-variety variable page](https://microdata.nigerianstat.gov.ng/index.php/catalog/173/variable/F21/V1595?name=s04_q03__1) shows a0–1 range but no reconciled selection/value mapping. Local release fields are modern/traditional with no0/1 value-label definitions; the inspected questionnaire Section4 lists three certification/variety options. These sources do not establish how that recoding was performed. The [released seed dictionary](https://microdata.nigerianstat.gov.ng/index.php/catalog/173/data-dictionary/F21?file_name=8_Seed_use_mainSeason) confirms the two field labels but does not resolve their relationship to the questionnaire. No modern/traditional/certified/improved-seed percentages are published. Source options independently have explicit0/1 labels, allowing this narrower source analysis to proceed.

The public questionnaire local hash remains `29a696d9764a1d8c70874a18d4e0b4d5f8d4b2d2ba6d8a7efaeabbd17ac4f676`; existing extracted Section4 text was inspected rather than adding a new PDF dependency. A release-specific recoding/codebook explanation is needed before reopening varieties. No messages were sent to NBS or others.

## Reproduce and limits

```powershell
.venv-m4/Scripts/python.exe -m agrisight.seed_sources data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/seed_sources_ss1.json
.venv-m4/Scripts/python.exe -m pytest -q
.venv-m4/Scripts/python.exe -m ruff check src tests scripts streamlit_app.py research_explorer_app.py
```

Exact category frequencies, complete-vector masks, row/type/household totals and coverage flags reconcile independently in Python/SQLite; shared key/code staging is disclosed. Reviewed hashes pin source/model/SQL/contract/label metadata/lock versions. The optional adapter verifies all arithmetic, shares, combination marginal bounds and household/crop-yes totals before conservative projection. Raw seed data and exact analytical JSON remain ignored; no quantities or live identifiers are exposed. Existing findings and map meaning are preserved. See the [delivery review](../docs/SEED_SOURCE_REVIEW.md). M6-04 release/privacy/permission/security gates remain open; no deployment or survey redistribution.
