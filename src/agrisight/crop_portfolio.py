"""CP1 temporary-crop roster portfolio, with independently checked household counts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
import zipfile
from collections import Counter
from importlib.resources import files
from numbers import Real
from pathlib import Path

import pandas as pd

from agrisight.e1_profile import ARCHIVE_SHA256, identifier, read_selected, response
from agrisight.nass01 import check_period

FIELDS = ("hhid", "s02_plotRoster__id", "s03_cropRoster__id", "s03_cropsType")
LABELS = dict(zip(FIELDS, ("Household ID", "Plot id", "Crop ID", "Crop Type"), strict=True))


def crop_labels() -> dict[int, str]:
    return {int(k): v for k, v in json.loads(files("agrisight").joinpath(
        "reporting/crop_labels_v1.json").read_bytes()).items()}


def sql_text() -> str:
    return files("agrisight").joinpath("sql/crop_portfolio.sql").read_text(encoding="utf-8")


def keys(frame: pd.DataFrame, columns: tuple) -> list[tuple]:
    if not frame.columns.is_unique or not set(columns).issubset(frame.columns):
        raise ValueError("Missing/duplicate required columns")
    rows = [tuple(identifier(v) for v in row) for row in frame[list(columns)].itertuples(index=False, name=None)]
    if any(None in row for row in rows) or len(rows) != len(set(rows)):
        raise ValueError("Missing/duplicate source key")
    return rows


def calculate(households: pd.DataFrame, plots: pd.DataFrame, crops: pd.DataFrame) -> dict:
    hh_keys = keys(households, ("hhid",))
    plot_keys = keys(plots, ("hhid", "s02_plotRoster__id"))
    crop_keys = keys(crops, FIELDS[:3])
    known, parent_plots = set(hh_keys), set(plot_keys)
    if any((hh,) not in known for hh, _ in plot_keys) or any(k[:2] not in parent_plots for k in crop_keys):
        raise ValueError("Orphan plot/crop record")
    if "s00_q15a" not in households or "s03_cropsType" not in crops:
        raise ValueError("Required response/type missing")
    household_rows = [(key[0], response(value)) for key, value in zip(hh_keys, households.s00_q15a, strict=True)]
    labels, rows = crop_labels(), []
    for key, code, kind in zip(crop_keys, crops.s03_cropRoster__id, crops.s03_cropsType, strict=True):
        if (not isinstance(code, Real) or isinstance(code, bool) or not math.isfinite(code) or code <= 0 or not float(code).is_integer()
                or not isinstance(kind, Real) or isinstance(kind, bool) or kind not in (1, 2) or (kind == 1 and code not in labels)):
            raise ValueError("Unknown/missing crop code or type")
        rows.append((*key[:2], int(code), int(kind)))
    pairs = {(hh, code) for hh, _, code, kind in rows if kind == 1}
    households_per_crop = Counter(code for _, code in pairs)
    per_household = Counter(hh for hh, _ in pairs)
    distribution = Counter(min(n, 5) for n in per_household.values())
    yes = {hh for hh, presence in household_rows if presence == "yes"}
    represented = set(per_household)
    summary = {"household_records": len(hh_keys), "plot_records": len(plot_keys), "crop_rows": len(rows),
        "temporary_rows": sum(kind == 1 for _, _, _, kind in rows),
        "excluded_permanent_rows": sum(kind == 2 for _, _, _, kind in rows),
        "unlabelled_permanent_rows": sum(kind == 2 and code not in labels for _, _, code, kind in rows),
        "represented_households": len(represented), "household_crop_pairs": len(pairs),
        "crop_yes_households_without_temporary_record": len(yes-represented),
        "temporary_households_without_crop_yes": len(represented-yes)}
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE households(hh TEXT PRIMARY KEY,presence TEXT)")
        db.execute("CREATE TABLE plots(hh TEXT,plot TEXT,PRIMARY KEY(hh,plot))")
        db.execute("CREATE TABLE crops(hh TEXT,plot TEXT,crop INTEGER,kind INTEGER,PRIMARY KEY(hh,plot,crop))")
        db.executemany("INSERT INTO households VALUES(?,?)", household_rows)
        db.executemany("INSERT INTO plots VALUES(?,?)", plot_keys)
        db.executemany("INSERT INTO crops VALUES(?,?,?,?)", rows)
        sql_crops = dict(db.execute(sql_text()))
        sql_diversity = dict(db.execute("WITH pairs AS (SELECT DISTINCT hh,crop FROM crops WHERE kind=1), "
            "sizes AS (SELECT hh,COUNT(*) n FROM pairs GROUP BY hh) SELECT MIN(n,5),COUNT(*) FROM sizes GROUP BY MIN(n,5)"))
        sql_counts = db.execute("SELECT (SELECT COUNT(*) FROM households),(SELECT COUNT(*) FROM plots),"
            "COUNT(*),COALESCE(SUM(kind=1),0),COALESCE(SUM(kind=2),0),COALESCE(SUM(CASE WHEN kind=2 AND crop NOT IN (" + ",".join(str(k) for k in labels) + ") THEN 1 ELSE 0 END),0),COUNT(DISTINCT CASE WHEN kind=1 THEN hh END) FROM crops").fetchone()
        sql_pairs = db.execute("SELECT COUNT(*) FROM (SELECT DISTINCT hh,crop FROM crops WHERE kind=1)").fetchone()[0]
        sql_unmatched_yes = db.execute("SELECT COUNT(*) FROM households WHERE presence='yes' AND hh NOT IN (SELECT hh FROM crops WHERE kind=1)").fetchone()[0]
        sql_unmatched_roster = db.execute("SELECT COUNT(DISTINCT c.hh) FROM crops c JOIN households h ON c.hh=h.hh WHERE c.kind=1 AND h.presence!='yes'").fetchone()[0]
    if (dict(households_per_crop) != sql_crops or dict(distribution) != sql_diversity
            or tuple(summary.values()) != (*sql_counts, sql_pairs, sql_unmatched_yes, sql_unmatched_roster)):
        raise ValueError("Portfolio SQL/Python disagreement")
    denominator = len(represented)
    return {"counts": summary, "mean_categories": len(pairs)/denominator if denominator else None,
        "portfolio": [{"code": code, "label": labels[code], "households": n,
                       "share": n/denominator} for code, n in sorted(households_per_crop.items())],
        "diversity": [{"categories": str(k) if k < 5 else "5+", "households": distribution[k],
                       "share": distribution[k]/denominator if denominator else None} for k in range(1, 6)]}


def run(archive_path: Path, output: Path) -> None:
    root = Path.cwd().resolve()
    if not output.resolve().is_relative_to(root / "reports/private"):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Unreviewed archive")
    with zipfile.ZipFile(archive_path) as archive:
        hh, _ = read_selected(archive, "1_households.dta", ("hhid", "s00_q15a", "mainAgSeason", "referenceAgYear"))
        check_period(hh)
        pp, _ = read_selected(archive, "3_Plot_mainSeason.dta", ("hhid", "s02_plotRoster__id"))
        cc, metadata = read_selected(archive, "4_Crop_mainSeason.dta", FIELDS)
        if metadata["selected_columns"] != LABELS:
            raise ValueError("Crop field labels changed")
        with archive.open("4_Crop_mainSeason.dta") as stream, pd.io.stata.StataReader(stream) as reader:
            labels = reader.value_labels()
            if labels.get("s03_cropRoster__id") != crop_labels() or labels.get("s03_cropsType") != {
                    1: "Temporary crop", 2: "Permanent/Continuous crop"}:
                raise ValueError("Crop category labels changed")
    provenance = {"model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sql_sha256": hashlib.sha256(sql_text().encode()).hexdigest(),
        "contract_sha256": hashlib.sha256((root / "docs/CROP_PORTFOLIO_CONTRACT.md").read_bytes()).hexdigest(),
        "labels_sha256": hashlib.sha256(files("agrisight").joinpath("reporting/crop_labels_v1.json").read_bytes()).hexdigest(),
        "lock_sha256": hashlib.sha256((root / "requirements/e1.lock").read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "pandas": pd.__version__, "sqlite": sqlite3.sqlite_version}
    result = {"version": "1.0", "source_sha256": digest, "provenance": provenance, **calculate(hh, pp, cc)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Crop portfolio aggregates saved under ignored reports/private")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
