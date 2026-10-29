# NASS design, reference periods and source disposition

Reviewed 2026-10-29. Evidence combines public documents, the owner-supplied archive and executed E1.1/E1.2. Review is technical, not owner signature or external certification.

## Methodology evidence

Downloaded [NBS report](https://microdata.nigerianstat.gov.ng/index.php/catalog/173/download/1299) to ignored `data/raw/nass_2023/documentation/report.pdf`: 12385265 bytes, SHA256 `0fb2343f300692b1e16146f944f86974e5302c5ff528c4c8e10a2ea94812ddeb`, 322 PDF pages. Inspected relevant methodology sections, not every published finding.

Report sections 2.1–2.2 (PDF pp.18–21, printed pp.8–11) describe agricultural-household sampling through enumeration areas and later household selection, with stratification, nonresponse adjustment and calibration. Section 2.2.4 specifies resampling-based uncertainty (bootstrap/jackknife). These requirements cannot be reconstructed from a positive final weight alone.

Section 2.13 (PDF p.25, printed p.15) specifies rainy season April–October 2022 and dry season November 2022–March 2023. The questionnaire (PDF p.5) instead references dry season 2021/2022. This is a source conflict, not evidence that one date can be silently corrected.

## Released-field comparison

All 21 Stata schemas were inspected using the reproducible E1.2 metadata scan. Name/label search for PSU, strata, cluster, replication, bootstrap, jackknife and enumeration/EA found only `ea_name` in forestry. No usable household/plot variance-design specification was identified; this search does not prove no alternative reconstruction is possible. Do not read or publish forestry EA names or treat them as household PSUs. That field also warrants disclosure review before any forestry work.

`final_weight` is present on household/plot files, but no verified replicate weights or linked household-level design contract is established. Geography labels (`zone_id`, `state_id`, `lga`, `sector`) are not interchangeable with design variables. No assumption of LGA precision or a substitution of LGA as PSU is justified by this review.

Across all 143105 household rows, reference fields have one nonmissing value each:

- `referenceAgYear`: 2022/2023 agricultural year.
- `mainAgSeason`: rainy season April–October 2022, consistent with the report.
- `minorAgSeason`: dry season November 2021–March 2022, inconsistent with report section 2.13 but consistent with questionnaire wording.

**Disposition:** main-season sample analysis may use the released April–October 2022 label. Keep original dry-season labels in raw inputs; defer cross-season comparisons and calendar-based dry-season interpretation pending producer clarification. Dry-season file-quality checks remain valid without assigning a resolved calendar year. Publication title is not the collection date; the catalogue's collection-date fields are not independently validated by these reference fields.

## Access and release contract

Owner created an NBS account, signed in, supplied the application snapshot and then reported downloading the archive. This is the owner-authorized research source used locally, not an independently observed login transaction. The application conditions were inspected and recorded in the [source card](NASS_2023_CARD.md). Restrict use to statistical/scientific aggregate research; no redistribution without written agreement, identifying linkage or reidentification. Cite NBS and retain the obligation to supply publication/report copies at the release stage. No message has been sent or public release performed.

Freeze input by the verified archive hash and member names in the [inventory](NASS_2023_INVENTORY.md). Local acquisition date is 2026-10-29; exact upstream download time and byte equivalence with a separately versioned mirror are **unknown**, not fabricated. No requirement to recover browser credentials or recreate a grant is imposed. If the owner later supplies additional grant conditions or a different release, review and version them before use.

## NASS versus GHS decision

Retain NASS for the first reproducible **main-season sample descriptive workflow**: the acquired household/plot fields and keys are verified, periods are usable for main season, and quality limits are observed. This does not approve population inference.

GHS remains a genuine alternative for a future service-access question: its [extension-services dictionary](https://microdata.worldbank.org/catalog/6410/data-dictionary/F41?file_name=sect11l1_plantingw5) documents `hhid`, `topic_cd`, `s11l1q1` (advice receipt) and `s11l1q2` (source). Topic rows must not be counted as different households. Its [catalogue](https://microdata.worldbank.org/catalog/6410) distinguishes cross-sectional and longitudinal weights. GHS microdata have not been acquired or quality-tested here. Do not switch sources solely to bypass the NASS issues or join surveys as one population; a new source needs its own acquisition/design contract.

## Explicit M2 gates

1. **Population claims:** verify actual PSU/strata/replicate information and weight applicability, then validate an uncertainty implementation; otherwise stay with clearly labelled sample descriptions.
2. **Dry-season comparisons:** resolve conflicting calendar references before temporal comparison.
3. **Input quantities/access:** investigate missing quantities and documented roster eligibility; do not substitute absent rows with non-use, missing quantities with zero, or quantity with access.
4. **Area-based measures:** review the 48 missing plot areas before area-based denominators/yields; do not impute to make the dataset complete.

These are recorded suitability outcomes and restrictions, not unperformed E1 results. Full source certification and every possible agricultural analysis are outside M1's first-workflow suitability decision.
