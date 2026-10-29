"""Missing-area bounds for the median of a fixed released main-season plot roster."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
import zipfile
from importlib.resources import files
from numbers import Real
from pathlib import Path

import pandas as pd

from agrisight.e1_profile import ARCHIVE_SHA256, identifier, is_missing, read_selected

COLUMNS = ("hhid", "s02_plotRoster__id", "s02_q15", "s02_q16a")
EXACT = ("total_plots", "observed_areas", "missing_areas", "middle_lower_rank",
         "middle_upper_rank", "status")
NUMERIC = ("observed_only_median_m2", "full_roster_lower_m2", "full_roster_upper_m2",
           "width_m2")


def sql_model() -> str:
    return files("agrisight").joinpath("sql/nass02.sql").read_text(encoding="utf-8")


def validated_rows(frame: pd.DataFrame) -> list[tuple[str, str, float | None]]:
    if not frame.columns.is_unique or not set(COLUMNS).issubset(frame.columns):
        raise ValueError("Missing required or duplicate columns")
    seen, rows = set(), []
    for hh, plot, status, area in frame[list(COLUMNS)].itertuples(index=False, name=None):
        key = (identifier(hh), identifier(plot))
        if None in key or key in seen:
            raise ValueError("Missing or duplicate plot key; no rows dropped")
        seen.add(key)
        if (is_missing(status) or not isinstance(status, Real) or isinstance(status, bool)
                or status not in (1, 2, 3)):
            raise ValueError("Unexpected plot status; eligibility review required")
        if is_missing(area):
            numeric = None
        elif not isinstance(area, Real) or isinstance(area, bool):
            raise TypeError("Expected numeric area; no coercion")
        elif not math.isfinite(area) or area < 0:
            raise ValueError("Negative/nonfinite area; no clipping or exclusions")
        else:
            numeric = float(area)
        rows.append((*key, numeric))
    return rows


def python_bounds(areas: list[float | None]) -> dict:
    known = sorted(v for v in areas if v is not None)
    total, observed = len(areas), len(known)
    missing = total-observed
    r1, r2 = (total+1)//2, (total+2)//2

    def value(rank: int) -> float | None:
        return known[rank-1] if 1 <= rank <= observed else None

    def average(a: float | None, b: float | None) -> float | None:
        return a/2+b/2 if a is not None and b is not None else None

    reference = average(value((observed+1)//2), value((observed+2)//2))
    low = average(0.0 if r1 <= missing else value(r1-missing),
                  0.0 if r2 <= missing else value(r2-missing)) if total else None
    high = average(value(r1), value(r2)) if total else None
    return {
        "total_plots": total, "observed_areas": observed, "missing_areas": missing,
        "middle_lower_rank": r1 if total else None,
        "middle_upper_rank": r2 if total else None,
        "observed_only_median_m2": reference, "full_roster_lower_m2": low,
        "full_roster_upper_m2": high,
        "status": "undefined" if not total else "unbounded" if r2 > observed else "bounded",
        "width_m2": high-low if high is not None and low is not None else None,
    }


def sql_bounds(rows: list[tuple[str, str, float | None]]) -> dict:
    with sqlite3.connect(":memory:") as db:
        db.row_factory = sqlite3.Row
        db.executescript(sql_model())
        db.executemany("INSERT INTO stg_nass_plot_area VALUES(?,?,?)", rows)
        return dict(db.execute("SELECT * FROM mart_nass02_bounds").fetchone())


def calculate(frame: pd.DataFrame) -> dict:
    rows = validated_rows(frame)
    reference = python_bounds([row[2] for row in rows])
    result = sql_bounds(rows)
    for name in EXACT:
        if reference[name] != result[name]:
            raise ValueError("Count/rank/status reconciliation failed")
    for name in NUMERIC:
        a, b = reference[name], result[name]
        same = a is None and b is None if a is None or b is None else math.isclose(
            a, b, abs_tol=1e-9, rel_tol=1e-12
        )
        if not same:
            raise ValueError("Median/bounds reconciliation failed")
    return {"estimates": result,
            "reconciliation": "exact counts/ranks/status; numeric abs1e-9, rel1e-12"}


def companion_audit(frame: pd.DataFrame) -> dict[str, int]:
    """Describe missing/zero companion values without converting or filling the target."""
    counts = {"companion_missing": 0, "companion_zero_when_m2_missing": 0,
              "companion_zero_when_m2_positive": 0}
    for area, acres in zip(frame.s02_q16a, frame.areaAcresPlot):
        if is_missing(acres):
            counts["companion_missing"] += 1
        elif acres == 0:
            if is_missing(area):
                counts["companion_zero_when_m2_missing"] += 1
            elif area > 0:
                counts["companion_zero_when_m2_positive"] += 1
    return counts


def run(archive_path: Path, output: Path) -> None:
    private = Path.cwd().resolve() / "reports/private"
    if not output.resolve().is_relative_to(private):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Archive hash mismatch")
    with zipfile.ZipFile(archive_path) as archive:
        frame, metadata = read_selected(archive, "3_Plot_mainSeason.dta",
                                        (*COLUMNS, "areaAcresPlot"))
    if metadata["selected_columns"]["s02_q16a"] != "Area of plot in square meter":
        raise ValueError("Area unit label differs from the contract")
    if metadata["selected_columns"]["areaAcresPlot"] != "Plot area in Acres":
        raise ValueError("Companion unit label differs from the contract")
    result = {
        "indicator": "NASS-02", "contract_version": "1.0", "model_version": "1.0",
        "source_sha256": digest, "member": "3_Plot_mainSeason.dta",
        "definition": {
            "target": "median released s02_q16a over all eligible main-season plot rows",
            "unit": "square metres as labelled; measurement lineage not verified",
            "eligibility": "plot status 1,2,3; complete unique composite plot keys",
            "period": "April-October 2022, frozen main-season release",
            "unknown_support": "nonnegative, no finite upper cap",
            "median_convention": "average two middle ranks for even N",
            "reference": "known-area-only median, not assumed to equal full-roster target",
            "inference": "unweighted sample identification bounds, not confidence intervals",
            "geography": "pooled released roster only",
            "corrections": "none; no companion-field backfill or imputation",
        },
        "provenance": {
            "sql_sha256": hashlib.sha256(sql_model().encode()).hexdigest(),
            "python_model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "lock_sha256": hashlib.sha256(Path('requirements/e1.lock').read_bytes()).hexdigest(),
            "python": sys.version.split()[0], "pandas": pd.__version__,
            "sqlite": sqlite3.sqlite_version,
        }, "field_dtypes": {name: metadata["selected_dtypes"][name]
                            for name in ("s02_q16a", "areaAcresPlot")},
        "companion_audit": companion_audit(frame), **calculate(frame),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print("NASS-02 aggregate bounds saved under ignored reports/private.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)


if __name__ == "__main__":
    main()
