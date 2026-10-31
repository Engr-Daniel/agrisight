# Public hosting of aggregate results — 2026-10-31

The owner asked to host the stakeholder website publicly. This review covers the
public-results scope of M6-04; it is not a release of survey data.

## Permission

- **Owner-confirmed (2026-10-31):** NBS does not object to sharing the dashboard
  results publicly when they are properly referenced, provided the downloaded data
  are not released. The NBS portal's Access conditions text did not load without a
  login during this review, so it was not independently read here.
- Reference used on every page footer and in About: *National Bureau of Statistics
  (NBS), Nigeria. Nigeria - National Agricultural Sample Survey 2023
  (NGA-NBS-NASS-2023-V01). NBS Microdata Catalogue,
  https://microdata.nigerianstat.gov.ng/index.php/catalog/173.* The site states that
  the analysis is AgriSight's, not an official NBS publication, and that microdata
  are not redistributed.
- State boundaries: GRID3/geoBoundaries, CC BY 4.0, attributed on the map
  (THIRD_PARTY_NOTICES.md).

## What is published

`public/agrisight_public_v1.json` (SHA256
`3147f03ed89f461f574b568f91f63584c40116689f031844e95b43fef3467b8b`) holds only the
six display bundles the website already shows (core, crop, seed, irrigation,
conditions, coverage). Each passed its adapter's hash pinning, validation, pooling
and suppression. `python -m agrisight.public_evidence` regenerates it and refuses
fixture, unavailable or identifying content.

Not published: NBS microdata, `data/`, `reports/private/` aggregate files (including
exact rare seed-source combinations, which the display pools), and the research
explorer's synthetic studies.

## Disclosure assessment

- No identifier fields (household, plot, respondent, coordinates); checked by code
  and by test. No household or farm locations.
- The only geographic table is state sample coverage; minimum 1,536 households.
- Seed combinations: six named groups (smallest 2,248 records) plus a pooled
  remainder.
- Some national counts are below 30 (for example 1 record reporting storage for one
  crop; 3 records naming a shock reason). They have no geography or other
  cross-classification, match the reviewed contracts, and are already displayed.
  Owner may choose a stricter threshold later.
- Secrets scan of tracked files: no token, key or password patterns. No microdata
  or private files tracked.

## Hosting

GitHub Pages serves static files only; this is a Streamlit (Python) app.
`public_app.py` runs the site in hosted mode, reading only the public file;
`streamlit_app.py` is unchanged for local use with private evidence.
`requirements.txt` installs the verified M4 pins plus this package.

Deploy on Streamlit Community Cloud (owner's account): New app → repository
`Engr-Daniel/agrisight`, branch `master`, main file `public_app.py`; Advanced
settings → Python 3.11. The local config keeps `server.address = 127.0.0.1` as a
tested privacy guard; if the host cannot connect because of it, change that one line
deliberately.

## Verification

443 tests pass (10 new hosted-mode tests: forbidden-field detection, public-only
reads, malformed or missing file fails closed, fixture refusal, committed file valid
and cited, every page rendered from the public file). Ruff clean. A local preview of
`public_app.py` was inspected: real figures, citation in footer and About.

## Deployment observed

Owner deployed on Streamlit Community Cloud: https://agrisight-demo.streamlit.app/
(main file `public_app.py`, branch `master`; the default `127.0.0.1` local config did
not prevent hosting). Observed 2026-10-31 in headless Chrome 156: health endpoint
`ok`; public visitors reach the app without signing in; Overview, Seed sources,
Water management and About render the real figures and citation at 1440 px and
390 px; 0 JavaScript exceptions; no horizontal overflow.

## Still open in M6-04

Dependency licence review; independent reading of the NBS Access conditions text.
