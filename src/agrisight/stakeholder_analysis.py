"""SA1: aggregate-only stakeholder analysis with independent Python/SQLite counts."""

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

from agrisight.e1_profile import (
    ARCHIVE_SHA256,
    identifier,
    is_missing,
    read_selected,
    response,
)
from agrisight.nass01 import check_period

ACTIVITIES = {
    "crops": ("s00_q15a", "Main-season crops", "April–October 2022"),
    "livestock": ("s00_q16", "Livestock / poultry", "2022/2023 agricultural year"),
    "fish_farming": ("s00_q17", "Fish farming / aquaculture", "2022/2023 agricultural year"),
    "fish_capture": ("s00_q18", "Fish capture", "2022/2023 agricultural year"),
}
LABELS = {
    "s00_q15a": "15a. Did you/any member of your HH grow crops during the mainAgSeason",
    "s00_q16": "16.Have you/any member of your HH raised livestock/poultry in AGYear",
    "s00_q17": "17.Have you/any member of your HH practiced FISH FARMING/AQUACULTUREin AGyear",
    "s00_q18": "18.Have you/any member of your HH practiced FISH HUNTING/CAPTUREin AgYear",
    "s02_q15": "During the [MAIN AG SEASON], is this [PLOT]:",
    "s02_q16a": "Area of plot in square meter",
}
TYPES = {1: "Cultivated conventional plot", 2: "Temporarily fallow conventional plot",
         3: "Kitchen garden / backyard"}
TYPE_LABELS = {1: "A conventional plot cultivated", 2: "A conventional plot left temporarily fallow",
               3: "A kitchen garden/backyard"}


def sql_text() -> str:
    return files("agrisight").joinpath("sql/stakeholder.sql").read_text(encoding="utf-8")


def require_columns(frame: pd.DataFrame, columns: tuple) -> None:
    if not frame.columns.is_unique or not set(columns).issubset(frame.columns):
        raise ValueError("Required columns missing or duplicated")


def calculate(households: pd.DataFrame, plots: pd.DataFrame) -> dict:
    fields = tuple(v[0] for v in ACTIVITIES.values())
    require_columns(households, ("hhid", *fields))
    require_columns(plots, ("hhid", "s02_plotRoster__id", "s02_q15", "s02_q16a"))
    hh, pp, known, plot_keys = [], [], set(), set()
    for row in households[["hhid", *fields]].itertuples(index=False, name=None):
        key = identifier(row[0])
        if key is None or key in known:
            raise ValueError("Missing/duplicate household key")
        known.add(key)
        hh.append((key, *(response(v) for v in row[1:])))
    for raw_key, raw_plot, kind, area in plots[
            ["hhid", "s02_plotRoster__id", "s02_q15", "s02_q16a"]].itertuples(
                index=False, name=None):
        key = (identifier(raw_key), identifier(raw_plot))
        if None in key or key in plot_keys or key[0] not in known:
            raise ValueError("Missing/duplicate/orphan plot key")
        plot_keys.add(key)
        if not isinstance(kind, Real) or isinstance(kind, bool) or kind not in TYPES:
            raise ValueError("Unknown plot type")
        missing = is_missing(area)
        if not missing and (not isinstance(area, Real) or isinstance(area, bool)
                            or not math.isfinite(area) or area < 0):
            raise ValueError("Invalid area")
        pp.append((*key, int(kind), int(missing)))
    py = {}
    for index, name in enumerate(ACTIVITIES, 1):
        counts = Counter(row[index] for row in hh)
        py[name] = (len(hh), *(counts[k] for k in ("yes", "no", "missing", "other")))
    joint = Counter((row[1], row[2]) for row in hh if row[1] in ("yes", "no")
                    and row[2] in ("yes", "no"))
    types = Counter(row[2] for row in pp)
    missing_areas = sum(row[3] for row in pp)
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE hh(id TEXT PRIMARY KEY,crops TEXT,livestock TEXT,"
                   "fish_farming TEXT,fish_capture TEXT)")
        db.execute("CREATE TABLE pp(hh TEXT,plot TEXT,kind INTEGER,missing INTEGER,"
                   "PRIMARY KEY(hh,plot), FOREIGN KEY(hh) REFERENCES hh(id))")
        db.executemany("INSERT INTO hh VALUES(?,?,?,?,?)", hh)
        db.executemany("INSERT INTO pp VALUES(?,?,?,?)", pp)
        sql = {row[0]: tuple(row[1:]) for row in db.execute(sql_text())}
        # Empty GROUP BY yields no rows: explicit zero counts, not fabricated observations.
        if not hh:
            sql = {name: (0, 0, 0, 0, 0) for name in ACTIVITIES}
        sql_joint = {(c, l): n for c, l, n in db.execute(
            "SELECT crops,livestock,COUNT(*) FROM hh WHERE crops IN ('yes','no') "
            "AND livestock IN ('yes','no') GROUP BY crops,livestock")}
        sql_types = dict(db.execute("SELECT kind,COUNT(*) FROM pp GROUP BY kind"))
        sql_area = db.execute("SELECT COUNT(*),COALESCE(SUM(missing),0) FROM pp").fetchone()
    if py != sql or dict(joint) != sql_joint or dict(types) != sql_types or (
            len(pp), missing_areas) != sql_area:
        raise ValueError("Independent SQL/Python reconciliation failed")
    activities = []
    for name, (_, label, period) in ACTIVITIES.items():
        total, yes, no, missing, invalid = py[name]
        valid = yes+no
        activities.append({"id": name, "label": label, "period": period, "input_rows": total,
                           "yes": yes, "no": no, "missing": missing, "invalid": invalid,
                           "denominator": valid, "share": yes/valid if valid else None})
    denominator = sum(joint.values())
    return {"activities": activities, "overlap": {
        "denominator": denominator, "excluded": len(hh)-denominator,
        "period": "Main-season crops (Apr–Oct 2022) × annual livestock (2022/2023)",
        "cells": [{"crops": c, "livestock": l, "count": joint[c, l]}
                  for c in ("yes", "no") for l in ("yes", "no")]},
        "plot_types": [{"code": code, "label": label, "count": types[code]}
                       for code, label in TYPES.items()],
        "plots": {"total": len(pp), "missing_area": missing_areas,
                  "recorded_area": len(pp)-missing_areas}}


def run(archive_path: Path, output: Path) -> None:
    root = Path.cwd().resolve()
    if not output.resolve().is_relative_to(root/"reports/private"):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Archive hash differs from input contract")
    with zipfile.ZipFile(archive_path) as archive:
        hh, hm = read_selected(archive, "1_households.dta", (
            "hhid", *(v[0] for v in ACTIVITIES.values()), "mainAgSeason", "referenceAgYear"))
        pp, pm = read_selected(archive, "3_Plot_mainSeason.dta", (
            "hhid", "s02_plotRoster__id", "s02_q15", "s02_q16a"))
        check_period(hh)
        for meta in (hm, pm):
            for field, label in meta["selected_columns"].items():
                if field in LABELS and LABELS[field] != label:
                    raise ValueError("Released field label differs")
        with archive.open("3_Plot_mainSeason.dta") as stream, pd.io.stata.StataReader(stream) as reader:
            if reader.value_labels().get("s02_q15") != TYPE_LABELS:
                raise ValueError("Plot category labels differ")
    result = {"analysis_version": "1.0", "source_sha256": digest,
              "scope": "Unweighted observed sample; no population uncertainty or geography",
              "provenance": {"python": sys.version.split()[0], "pandas": pd.__version__,
                  "sqlite": sqlite3.sqlite_version,
                  "model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "sql_sha256": hashlib.sha256(sql_text().encode()).hexdigest(),
                  "contract_sha256": hashlib.sha256((root/'docs/STAKEHOLDER_ANALYTICS_BRIEF.md')
                                                     .read_bytes()).hexdigest(),
                  "lock_sha256": hashlib.sha256((root/'requirements/e1.lock').read_bytes())
                                         .hexdigest()}, **calculate(hh, pp)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding="utf-8")
    print("Stakeholder survey aggregates saved under ignored reports/private")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
