"""Bounded NASS E1.1 checks; no row-level output or population inference."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sqlite3
import zipfile
from numbers import Integral, Real
from pathlib import Path

import pandas as pd
from pandas.io.stata import StataMissingValue

ARCHIVE_SHA256 = "a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02"
HOUSEHOLD_COLUMNS = ("hhid", "final_weight")
PLOT_COLUMNS = ("hhid", "s02_plotRoster__id", "s02_q07", "final_weight")


def is_missing(value: object) -> bool:
    """Treat ordinary and Stata tagged missing as missing, without treating 0 as missing."""
    return isinstance(value, StataMissingValue) or bool(pd.isna(value))


def identifier(value: object) -> str | None:
    """Canonicalize numeric identifiers; keep nonblank strings exact and type-distinct."""
    if is_missing(value) or (isinstance(value, str) and not value.strip()):
        return None
    if isinstance(value, str):
        return "s:" + value
    if isinstance(value, Integral) and not isinstance(value, bool):
        return "n:" + str(value)
    if isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value):
        if float(value).is_integer():
            return "n:" + str(int(value))
        return "n:" + format(float(value), ".17g")
    raise ValueError("Unsupported identifier type; no identifier values logged")


def response(value: object) -> str:
    if is_missing(value):
        return "missing"
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError("Expected numeric Stata response codes")
    return "yes" if value == 1 else "no" if value == 2 else "other"


def weight_checks(values: pd.Series) -> dict[str, int]:
    result = dict.fromkeys(("missing", "nonfinite", "nonpositive", "positive_finite"), 0)
    for value in values:
        if is_missing(value):
            result["missing"] += 1
        elif not isinstance(value, Real) or isinstance(value, bool):
            raise ValueError("Expected numeric weights")
        elif not math.isfinite(value):
            result["nonfinite"] += 1
        elif value <= 0:
            result["nonpositive"] += 1
        else:
            result["positive_finite"] += 1
    return result


def profile_frames(households: pd.DataFrame, plots: pd.DataFrame) -> dict:
    """Compute integer quality measures and independently reconcile them in SQLite."""
    for frame, required in ((households, HOUSEHOLD_COLUMNS), (plots, PLOT_COLUMNS)):
        if not set(required).issubset(frame.columns) or not frame.columns.is_unique:
            raise ValueError("Missing required columns or duplicated column names")

    hh = pd.DataFrame({"hhid": households.hhid.map(identifier)})
    pp = pd.DataFrame({
        "hhid": plots.hhid.map(identifier),
        "plot_id": plots.s02_plotRoster__id.map(identifier),
        "response": plots.s02_q07.map(response),
    })
    complete = pp.dropna(subset=["hhid", "plot_id"])
    hcomplete = hh.dropna()
    known = set(hcomplete.hhid)
    categories = pp.response.value_counts()
    metrics = {
        "household_rows": len(hh),
        "household_missing_key_rows": int(hh.hhid.isna().sum()),
        "household_distinct_complete_keys": int(hcomplete.hhid.nunique()),
        "household_duplicate_excess": len(hcomplete) - int(hcomplete.hhid.nunique()),
        "plot_rows": len(pp),
        "plot_missing_key_rows": len(pp) - len(complete),
        "plot_distinct_complete_keys": len(complete.drop_duplicates(["hhid", "plot_id"])),
        "plot_duplicate_excess": len(complete) - len(
            complete.drop_duplicates(["hhid", "plot_id"])
        ),
        "plot_missing_household_id_rows": int(pp.hhid.isna().sum()),
        "orphan_plot_rows": int((pp.hhid.notna() & ~pp.hhid.isin(known)).sum()),
        **{f"irrigation_{key}": int(categories.get(key, 0))
           for key in ("yes", "no", "missing", "other")},
    }
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE hh(hhid TEXT)")
        db.execute("CREATE TABLE pp(hhid TEXT, plot_id TEXT, response TEXT NOT NULL)")
        db.executemany("INSERT INTO hh VALUES(?)", hh.itertuples(index=False, name=None))
        db.executemany("INSERT INTO pp VALUES(?,?,?)", pp.itertuples(index=False, name=None))
        queries = {
            "household_rows": "SELECT COUNT(*) FROM hh",
            "household_missing_key_rows": "SELECT COUNT(*) FROM hh WHERE hhid IS NULL",
            "household_distinct_complete_keys": "SELECT COUNT(DISTINCT hhid) FROM hh",
            "household_duplicate_excess": (
                "SELECT COUNT(hhid)-COUNT(DISTINCT hhid) FROM hh"
            ),
            "plot_rows": "SELECT COUNT(*) FROM pp",
            "plot_missing_key_rows": (
                "SELECT COUNT(*) FROM pp WHERE hhid IS NULL OR plot_id IS NULL"
            ),
            "plot_distinct_complete_keys": (
                "SELECT COUNT(*) FROM (SELECT DISTINCT hhid,plot_id FROM pp "
                "WHERE hhid IS NOT NULL AND plot_id IS NOT NULL)"
            ),
            "plot_missing_household_id_rows": "SELECT COUNT(*) FROM pp WHERE hhid IS NULL",
            "orphan_plot_rows": (
                "SELECT COUNT(*) FROM pp WHERE hhid IS NOT NULL AND NOT EXISTS "
                "(SELECT 1 FROM hh WHERE hh.hhid=pp.hhid)"
            ),
            "plot_duplicate_excess": (
                "SELECT COALESCE(SUM(n-1),0) FROM (SELECT COUNT(*) n FROM pp "
                "WHERE hhid IS NOT NULL AND plot_id IS NOT NULL GROUP BY hhid,plot_id)"
            ),
            **{f"irrigation_{key}": f"SELECT COUNT(*) FROM pp WHERE response='{key}'"
               for key in ("yes", "no", "missing", "other")},
        }
        # This index changes execution cost, not the count or join denominator.
        db.execute("CREATE INDEX hh_id ON hh(hhid)")
        sql = {key: db.execute(query).fetchone()[0] for key, query in queries.items()}
    if metrics != sql:
        raise ValueError("Independent SQL reconciliation failed; no report produced")
    return {
        "counts": metrics, "sql_reconciliation": "exact match for all integer counts",
        "household_weights": weight_checks(households.final_weight),
        "plot_weights": weight_checks(plots.final_weight),
    }


def read_selected(archive: zipfile.ZipFile, member: str, columns: tuple) -> tuple:
    """Read fixed members only; never extract the archive or expose record samples."""
    if archive.namelist().count(member) != 1:
        raise ValueError("Expected exactly one copy of each required archive member")
    with pd.io.stata.StataReader(io.BytesIO(archive.read(member))) as reader:
        labels = reader.variable_labels()
        if not set(columns).issubset(labels):
            raise ValueError("Required schema differs from the documented contract")
        frame = reader.read(columns=list(columns), convert_categoricals=False,
                            convert_missing=True)
        metadata = {
            "variables_in_file": len(labels),
            "selected_columns": {name: labels[name] for name in columns},
            "selected_dtypes": {name: str(dtype) for name, dtype in frame.dtypes.items()},
        }
    return frame, metadata


def run(archive_path: Path, output: Path) -> None:
    """Write aggregate machine output only within this checkout's ignored report area."""
    private = (Path.cwd() / "reports/private").resolve()
    if not output.resolve().is_relative_to(private):
        raise ValueError("Output must be inside reports/private in the current checkout")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Archive hash differs from the acquired input contract")
    with zipfile.ZipFile(archive_path) as archive:
        households, hhmeta = read_selected(archive, "1_households.dta", HOUSEHOLD_COLUMNS)
        plots, pmeta = read_selected(archive, "3_Plot_mainSeason.dta", PLOT_COLUMNS)
    result = {
        "protocol": "E1.1", "source": "NASS owner-supplied real survey archive",
        "sha256": digest, "pandas": pd.__version__,
        "scope": "Unweighted sample quality counts; no population inference or row output",
        "schema": {"households": hhmeta, "plots": pmeta},
        **profile_frames(households, plots),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
    print("E1.1 aggregate checks saved to ignored reports/private output.")


if __name__ == "__main__":
    main()
