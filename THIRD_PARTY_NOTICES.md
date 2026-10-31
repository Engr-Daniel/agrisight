# Third-party geographic data

The application source licence does not replace the licence of the following public boundary data.

## Nigeria state/FCT boundaries

- Files: `src/agrisight/reporting/nigeria_adm1_v1.json` and `nigeria_adm1_source_metadata_v1.json`.
- Attribution: GRID3, distributed through William & Mary geoLab / geoBoundaries gbOpen. Boundary ID `NGA-ADM1-27671186`; year represented2022; 37 ADM1 units.
- Source: [geoBoundaries metadata](https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/); [commit-pinned simplified GeoJSON](https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/NGA/ADM1/geoBoundaries-NGA-ADM1_simplified.geojson).
- Licence: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), as reported by the boundary metadata. Attribution, licence link and modifications are retained in the resource and the displayed map. No endorsement is implied. Data are provided without a warranty of boundary or cadastral accuracy.
- Changes: use the upstream simplified boundary geometry, normalize ring orientation for D3 rendering, remove unrelated source properties and apply an explicitly reviewed survey-state name/code crosswalk, including FCT ↔ Abuja Federal Capital Territory. Source coordinate precision is retained. These coordinates describe public administrative boundaries, never survey household or farm locations.
- Reproduction: `scripts/prepare_nigeria_boundaries.py` reads the downloaded public GeoJSON and the frozen source-metadata JSON. Source and transformed hashes are recorded in the resource and reviewed coverage manifest.

This licence concerns public boundary data only. It does not grant redistribution
rights over NASS microdata. Private analytical artifacts remain in ignored storage;
the public site uses a separately reviewed display-only result bundle under the
owner-confirmed public-results permission. See the scoped, completed
[hosting review](docs/PUBLIC_HOSTING_REVIEW.md).

## Application dependencies

AgriSight's MIT licence does not replace dependency copyrights, licences or NOTICE
terms. The [45-package licence review](docs/DEPENDENCY_LICENSE_REVIEW.md) records
installed declarations and shipped notices, including composite licences and
packaging limitations. Dependencies are installed from upstream distributions,
not vendored into this repository. Preserve applicable upstream notices when
redistributing or modifying those components.
