# E1.2 — M1 suitability extension

Specified 2026-10-29 before extended record-level checks. Builds on [E1.1](E1_PROTOCOL.md); it does not turn the study into a full audit of every agricultural module.

## Scope and rules

- Inventory all 21 released Stata schemas/labels to identify candidate design fields. A name/label search is evidence of available metadata, not proof a survey design can be reconstructed. Read no unrestricted record samples.
- Household activity codes (`s00_q15a`, `s00_q15b`, `s00_q16`, `s00_q17`, `s00_q18`): classify 1=yes, 2=no, tagged/ordinary missing, other; check corresponding file value labels. No causes inferred from responses.
- Inspect only allow-listed reference strings (`referenceAgYear`, `mainAgSeason`, `minorAgSeason`) for comparison with report section 2.13. Any differences remain explicitly unresolved, not silently relabelled.
- Main-season irrigation: among yes responses, method/source codes are required; among no responses questionnaire skips them. Count missing applicable and populated non-applicable fields separately. Source codes define allowed categories; never count skipped questions as ordinary incompleteness. Unknown codes are review flags, not automatic deletion.
- Dry-season plot keys and infrastructure responses: repeat E1.1 integer counts and independent SQL checks with the documented dry-season field names. Do not pool seasons or claim separate unique farmers from plot rows.
- Input records: candidate key household + input type; count rows, missing/duplicate keys and orphan household IDs, then ordinary/tagged missing, nonfinite, negative, zero and positive quantities. The quantity field's kg label requires documentation review; no quantity totals or use/access prevalence. Zero quantities are review items, not automatically invalid.
- Flag nonpositive/nonfinite/missing plot area separately; plot roster includes temporarily fallow plots, so no arbitrary universal minimum-area exclusion.

All row-level work remains in memory, fixed archive members only, archive hash required. Machine outputs remain ignored under `reports/private/`. No source records changed, imputed or excluded. Integer key/response results are reconciled with SQLite through E1.1; extended skip flags are additional descriptive checks, not independently validated population estimates.

## Completion decision

M1's output is a scoped source-suitability decision and reproducible quality baseline, not a promise that every candidate question or all 21 modules are analytically ready. Record source unknowns honestly (including actual upstream transaction time); a local hash/version contract establishes the exact analysed input without inventing an upstream release certificate.

If variance design/period evidence is insufficient, explicitly limit the selected indicator to unweighted sample description and carry a named E2 gate. Do not infer precision from LGA/state availability, substitute LGA as PSU, use household weights as plot weights by assumption, or silently invent replicate weights. Unsupported/deferred questions remain so in the final feasibility matrix. Preserve any genuinely unmet M1 requirement as open rather than changing it to force completion.
