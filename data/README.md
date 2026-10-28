# Local data storage

All contents of `data/` except this README are ignored by Git. Use separate origins:

```text
data/raw/<source>/<release>/       immutable authorized survey downloads
data/interim/<source>/<release>/   reproducible intermediate row-level files
data/curated/<source>/<release>/   checked row-level analytical files
data/synthetic/<experiment>/      labelled seeded engineering records
```

These directories do not contain acquired datasets yet. Create them when needed. Never pool survey and synthetic populations. Do not commit restricted data by force-adding ignored files. Ignore rules do not remove previously tracked files or provide encryption/access control.

Reviewed tiny synthetic fixtures belong in code/tests rather than ignored working storage. Their methods, labels and privacy handling must be reviewed before committing. See the [data policy](../docs/DATA_POLICY.md).

Before acquisition: verify actual access terms; use authorized copies only; record filenames, release/version, download date, SHA256 and permissions in a reviewed non-identifying source manifest. Keep raw inputs unchanged and log transformations/corrections. Do not put credentials in manifests or commands.

Keep private exploratory exports in ignored `reports/private/`; publishable aggregates require a separate licence/disclosure review and explicit owner authorization. Clear notebook outputs before committing; row-level output must not leak into reports, notebooks or CI artifacts.

Verify before adding files:

```bash
git check-ignore --no-index data/raw/source/release/example.csv
git ls-files data
```

The first command should identify the ignored path; the second should contain only this README once tracked. These controls are preventive, not proof that data acquisition is authorized.
