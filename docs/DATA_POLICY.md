# Data, provenance and privacy policy

## Separation rule
1. **Official anonymized survey data:** use only with documented licence/access terms, source, vintage, unit of observation, weighting, collection method, geographic representativeness and known limitations. Anonymous != unrestricted redistribution.
2. **Synthetic operational data:** generated from documented assumptions and seeded scripts. Mark every output and screenshot **SYNTHETIC DEMONSTRATION DATA**.
3. **Restricted client data:** prohibited in this repository, including any Petgrave.io or Arzikin Noma Africa data, forms, screenshots, contracts or unpublished materials unless separately authorized (default: do not include).

Do not merge official survey samples and 55k synthetic profiles into a single real-world statistical population. Independent analyses may be presented side by side with clear source labels.

## Official source candidates — not yet licensed/ingested
- Nigeria National Agricultural Sample Survey 2023: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
- Nigeria General Household Survey Panel 2023–2024: https://microdata.nigerianstat.gov.ng/index.php/catalog/82

These are **candidates**, not verified download permissions or confirmed fitness for Nasarawa-level conclusions. Record the actual distribution terms, sampling geography, weights, coverage, missingness and interpretation before use.

## Sensitive and location fields
- Do not commit actual names, phones, emails, respondent IDs, household coordinates or exact farm locations.
- Prefer public administrative boundaries, aggregation and coarsened geographic bins.
- For a live demo, use aggregate/synthetic non-identifying material only.
- Deny small-count drill-downs when re-identification is plausible.
- Keep secrets in local environment stores, not `.env` in Git or screenshots.

## Quality and provenance
For each source record: track source identifier (non-identifying), schema version, extraction date, transform version, checks performed, correction history and analytical scope. Preserve raw inputs without silent overwrites.

## Before a public release
Complete a privacy review, licence review, threat model, dependency/secrets scan, aggregation disclosure test, and explicit owner approval. Private status alone does not justify handling restricted personal data.
