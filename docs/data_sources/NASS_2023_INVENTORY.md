# NASS archive acquisition inventory

Recorded: 2026-10-29. Owner reports downloading from NBS and supplied a Drive folder. This inventory used the existing local Downloads copy, not a completed Drive transfer. Drive listing confirmed the same filename and byte size; byte identity with the Drive copy was not verified.

## Provenance and integrity

- Archive: `NASS_anonymized_dataset.zip`
- Size: 118711951 bytes.
- SHA256: `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`
- Ignored immutable copy: `data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip`
- Ignored manifest: same directory, `acquisition_manifest.json`.
- Local source/copy SHA256 matched; ZIP CRC verification passed all 21 members.
- Total uncompressed file size: 2163973481 bytes. No archive members have been extracted or rewritten.
- File-format release byte: Stata 115 for all members. This is a serialization format, **not** an upstream study/release version.
- Owner-reported upstream study: `NGA-NBS-NASS-2023-v01`. Exact upstream download time, release metadata and any additional download-specific terms still need confirmation. Observed application restrictions are recorded in the [source card](NASS_2023_CARD.md).

The archive and manifest are ignored; no respondent data, values, IDs, Drive sharing links or credentials are committed. No sharing permissions were changed. The Drive connector's completed folder listing establishes file metadata only; its subsequent raw fetch was stopped once a matching local copy was found and used.

## Header inventory

Counts below were decoded from Stata binary headers using Python standard-library `zipfile` and `struct`: format byte 115, byte order in byte 1, variable count bytes 4?5, row count bytes 6?9 (zero-based). They are **header declarations**, not parsed-record quality findings or distinct people. Confirm with the chosen Stata reader during E1. Do not sum rows across modules as people; units and keys differ.

| Archive member | Rows declared in header | Variables declared in header |
|---|---:|---:|
| 1_households.dta | 143,105 | 254 |
| 2_hh_member.dta | 710,132 | 17 |
| 3_Plot_mainSeason.dta | 273,887 | 27 |
| 4_Crop_mainSeason.dta | 480,393 | 248 |
| 5_Harvest_mainSeason.dta | 334,133 | 68 |
| 6_Permanent_Crops.dta | 99,775 | 75 |
| 7_Harvested_PermCrops.dta | 56,359 | 69 |
| 8_Seed_use_mainSeason.dta | 414,049 | 21 |
| 9_Input_use_mainSeason.dta | 321,103 | 9 |
| 10_Plots_drySeason.dta | 26,524 | 25 |
| 11_Crops_drySeason.dta | 34,891 | 220 |
| 12_Harvest_drySeason.dta | 18,012 | 69 |
| 13_Seed_use_drySeason.dta | 31,473 | 17 |
| 14_Input_use_drySeason.dta | 30,787 | 8 |
| 15_Livestock.dta | 316,286 | 70 |
| 16_Livestock_products.dta | 18,652 | 13 |
| 17_Fish_Farming.dta | 3,761 | 13 |
| 18_Fish_Capture.dta | 13,326 | 18 |
| 19_Forestry_production.dta | 34,035 | 14 |
| 20_Labor.dta | 621,618 | 15 |
| 21_Holdings.dta | 3,856 | 8 |

## Verification commands

From the repository root, use the local Python 3.11 environment:

```powershell
.\.venv\Scripts\python.exe -m zipfile -t data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip
Get-FileHash -Algorithm SHA256 data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip
git check-ignore data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip
git ls-files data
```

CRC detects archive corruption; SHA256 identifies this local byte stream. Neither independently certifies NBS authenticity, permissions, anonymization quality or statistical correctness.

## Next increment

Select and lock a Stata-compatible reader, independently confirm metadata on the household and main-season plot files, then finalize the E1 protocol. Check schema/labels, candidate keys, joins, missing-value conventions, weight fields and design support without displaying respondent rows. Start with plot irrigation-infrastructure response quality; no agricultural estimate or confidence interval is produced by this inventory.
