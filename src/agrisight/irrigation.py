"""IR1: plot infrastructure and eligible main-method/water-source responses."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import zipfile
from collections import Counter
from importlib.resources import files
from numbers import Real
from pathlib import Path

import pandas as pd

from agrisight.e1_profile import ARCHIVE_SHA256, identifier, is_missing, read_selected, response
from agrisight.nass01 import check_period

LABELS = {"s02_q07": "Is there any irrigation infrastructure on this [PLOT]?",
          "s02_q08": "What is the main irrigation method used for [PLOT]?",
          "s02_q09": "Which is the main source of irrigation water on [PLOT]?"}
METHODS = {1: "Surface irrigation (flooding, furrows)", 2: "Sprinkler irrigation", 3: "Drip irrigation",
           4: "Spray or microsprinkler irrigation", 5: "Bubbler irrigation",
           6: "Equipped wetland and inland valley bottoms", 7: "Equipped flood recession cultivation",
           8: "Spate irrigation", 99: "Other ( Specify)"}
SOURCES = {1: "On-farm ground water", 2: "On-farm surface water",
           3: "Off-farm surface water (lakes, rivers, watercourses)",
           4: "Municipal water supply or other water network", 5: "Treated waste water",
           6: "Reservoir (used to avoid flooding)", 99: "Other ( Specify)"}


def sql_text() -> str:
    return files("agrisight").joinpath("sql/irrigation.sql").read_text(encoding="utf-8")


def category(value: object, labels: dict) -> str:
    if is_missing(value):
        return "missing"
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError("Expected numeric categorical response")
    return str(int(value)) if value in labels else "invalid"


def calculate(households: pd.DataFrame, plots: pd.DataFrame) -> dict:
    required = ("hhid", "s02_plotRoster__id", "s02_q15", *LABELS)
    if (not households.columns.is_unique or "hhid" not in households or not plots.columns.is_unique
            or not set(required).issubset(plots.columns)):
        raise ValueError("Missing/duplicate required columns")
    parents = [identifier(v) for v in households.hhid]
    known = set(parents)
    if None in known or len(known) != len(parents):
        raise ValueError("Missing/duplicate household key")
    rows, keys = [], set()
    for hh, plot, kind, presence, method, source in plots[list(required)].itertuples(index=False, name=None):
        key = (identifier(hh), identifier(plot))
        if None in key or key in keys or key[0] not in known:
            raise ValueError("Missing/duplicate/orphan plot key")
        if not isinstance(kind, Real) or isinstance(kind, bool) or kind not in (1, 2, 3):
            raise ValueError("Unknown plot type")
        keys.add(key)
        rows.append((*key, response(presence), category(method, METHODS), category(source, SOURCES)))
    presence = Counter(row[2] for row in rows)
    counters = {"presence": dict(presence)}
    skips = {}
    for name, index in (("method", 3), ("source", 4)):
        counters[name] = dict(Counter(row[index] for row in rows if row[2] == "yes"))
        skips[name] = sum(row[2] != "yes" and row[index] != "missing" for row in rows)
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE plots(hh TEXT,plot TEXT,presence TEXT,method TEXT,source TEXT,PRIMARY KEY(hh,plot))")
        db.executemany("INSERT INTO plots VALUES(?,?,?,?,?)", rows)
        independent = {name: {} for name in counters}
        for name, code, n in db.execute(sql_text()):
            independent[name][code] = n
        sql_skips = {name: db.execute(f"SELECT COUNT(*) FROM plots WHERE presence!='yes' AND {name}!='missing'").fetchone()[0]
                     for name in ("method", "source")}
    if counters != independent or skips != sql_skips:
        raise ValueError("Irrigation SQL/Python mismatch")
    valid = presence["yes"] + presence["no"]
    result = {"infrastructure": {"input_rows": len(rows), "yes": presence["yes"], "no": presence["no"],
        "missing": presence["missing"], "invalid": presence["other"], "denominator": valid,
        "share": presence["yes"]/valid if valid else None}}
    for name, labels in (("method", METHODS), ("source", SOURCES)):
        counts = counters[name]
        eligible = presence["yes"]
        missing, invalid = counts.get("missing", 0), counts.get("invalid", 0)
        valid = eligible-missing-invalid
        result[name] = {"eligible": eligible, "denominator": valid, "missing": missing, "invalid": invalid,
            "outside_yes": len(rows)-eligible, "populated_outside_yes": skips[name],
            "categories": [{"code": code, "label": label, "count": counts.get(str(code), 0),
                "share": counts.get(str(code), 0)/valid if valid else None} for code, label in labels.items()]}
    return result


def run(archive_path: Path, output: Path) -> None:
    root = Path.cwd().resolve()
    if not output.resolve().is_relative_to(root / "reports/private"):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Unreviewed archive")
    with zipfile.ZipFile(archive_path) as archive:
        hh, _ = read_selected(archive, "1_households.dta", ("hhid", "mainAgSeason", "referenceAgYear"))
        check_period(hh)
        pp, metadata = read_selected(archive, "3_Plot_mainSeason.dta", (
            "hhid", "s02_plotRoster__id", "s02_q15", *LABELS))
        if any(metadata["selected_columns"][k] != v for k, v in LABELS.items()):
            raise ValueError("Irrigation field labels changed")
        with archive.open("3_Plot_mainSeason.dta") as stream, pd.io.stata.StataReader(stream) as reader:
            labels = reader.value_labels()
            for field, expected in (("s02_q07", {1: "YES", 2: "NO"}), ("s02_q08", METHODS), ("s02_q09", SOURCES)):
                if labels.get(field) != expected:
                    raise ValueError("Irrigation category labels changed")
    result = {"version": "1.0", "source_sha256": digest, "provenance": {
        "model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sql_sha256": hashlib.sha256(sql_text().encode()).hexdigest(),
        "contract_sha256": hashlib.sha256((root / "docs/IRRIGATION_CONTRACT.md").read_bytes()).hexdigest(),
        "lock_sha256": hashlib.sha256((root / "requirements/e1.lock").read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "pandas": pd.__version__, "sqlite": sqlite3.sqlite_version},
        **calculate(hh, pp)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Irrigation aggregates saved under ignored reports/private")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
