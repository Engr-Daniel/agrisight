# M0-05: runnable comparison experiment

Date: 2026-10-26. Status: first actual framework execution verified on GitHub Actions; semantic parity still incomplete.

## Purpose
Compare Pandera (Python DataFrame contract) and Great Expectations (GX Core expectations) with the same synthetic valid and invalid input rows.

## Run locally
```bash
python -m pip install -e ".[dev]"
python -m pip install "pandas>=2.2,<3" "pandera[pandas]>=0.25,<1" "great_expectations>=1.6,<2"
python -m agrisight.framework_comparison
```
Alternatively, run the **M0 Validation Framework Comparison** workflow manually in GitHub Actions; it is intentionally NOT automatic on every push to keep initial CI lightweight.

## Expected output (hypothesis until observed)
- Pandera: valid true; invalid false.
- GX partial contract: valid true; invalid false.
- Installed versions printed; a passing exit status proves only that these fixtures behave as expected.

## Comparability limitation
Pandera checks all five fields including strict bool and nonempty strings. The GX proof of concept checks non-null person IDs, allowed kind/status and unique role identifiers, **but does not yet test empty-string IDs or strict boolean**. Thus this is a *partial smoke comparison*, not a performance or full-semantic-parity benchmark. Add equivalent checks, inspect structured failure details, and repeat with matched contracts before choosing a winner.

## Observed execution evidence (2026-10-26)
GitHub Actions run: https://github.com/Engr-Daniel/agrisight/actions/runs/40355059389
Commit tested: a2a4ba6. Environment: Python 3.11; pandas 2.3.3; Pandera 0.35.0; GX Core 1.24.1. Both frameworks returned **valid=true, invalid=false**, and the comparison step exited successfully. This confirms the implemented *partial* checks on two tiny synthetic inputs, not equivalent contracts or statistically meaningful benchmark performance. The same commit's foundation lint job failed for an import-order issue; a subsequent commit fixed this, and foundation CI succeeded at commit 61f1104.

## Further evidence required
Copy the exact workflow run link and environment versions into this report, inspect failure outputs, then compare readability, completeness, diagnostic details and runtime. Do not declare the comparison complete solely because a CI task exists.

## Research sources
- https://pandera.readthedocs.io/en/latest/dataframe_schemas.html
- https://docs.greatexpectations.io/docs/core/introduction/try_gx/
