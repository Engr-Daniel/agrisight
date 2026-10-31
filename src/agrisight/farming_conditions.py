"""FC1: four scoped stakeholder questions, independently reconciled in SQLite."""

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

from agrisight.crop_portfolio import keys
from agrisight.e1_profile import ARCHIVE_SHA256, is_missing, read_selected
from agrisight.nass01 import check_period

MODULES = ("3_Plot_mainSeason.dta", "4_Crop_mainSeason.dta",
           "5_Harvest_mainSeason.dta", "9_Input_use_mainSeason.dta")
BRANCHES = (("nonvegetable", "s01a_q07", "s01a_q11", "s01a_q16", "s01a_q08__", "s01a_q17__"),
            ("vegetable", "s01h_q08", "s01h_q16", "s01h_q21", "s01h_q09__", "s01h_q22__"))


def metadata() -> dict:
    return json.loads(files("agrisight").joinpath("reporting/conditions_labels_v1.json").read_bytes())


def sql_text() -> str:
    return files("agrisight").joinpath("sql/farming_conditions.sql").read_text(encoding="utf-8")


def numeric(value: object) -> float | None:
    if is_missing(value):
        return None
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError("Expected numeric response; no raw values logged")
    return float(value)


def calculate(households: pd.DataFrame, plots: pd.DataFrame, crops: pd.DataFrame,
              harvest: pd.DataFrame, inputs: pd.DataFrame) -> dict:
    """No row-level outputs; nulls never become zero or negative answers."""
    reference = metadata()
    frames = [plots, crops, harvest, inputs]
    key_fields = [("hhid", "s02_plotRoster__id"),
                  ("hhid", "s02_plotRoster__id", "s03_cropRoster__id"),
                  ("hhid", "s01b_harvestedCrops__id"), ("hhid", "s03c_inputType__id")]
    hh_keys = set(keys(households, ("hhid",)))
    source_keys = []
    normalized = []
    for frame, module, fields in zip(frames, MODULES, key_fields, strict=True):
        if not set(reference[module]["labels"]).issubset(frame.columns):
            raise ValueError("Missing required columns")
        kk = keys(frame, fields)
        if any((k[0],) not in hh_keys for k in kk):
            raise ValueError("Orphan household")
        source_keys.append(kk)
        normalized.append(pd.DataFrame({k: frame[k].map(numeric) for k in reference[module]["labels"] if k != "hhid"}))
    pp, cc, hh, ii = normalized
    parent_plots = set(source_keys[0])
    if any(k[:2] not in parent_plots for k in source_keys[1]):
        raise ValueError("Orphan crop")
    if not cc.s03_cropsType.isin([1, 2]).all():
        raise ValueError("Unknown crop type")
    crop_codes = reference[MODULES[1]]["value_labels"]["s03_cropRoster__id"]
    for code in cc.loc[cc.s03_cropsType.eq(1), "s03_cropRoster__id"]:
        if code is None or not math.isfinite(code) or str(int(code)) not in crop_codes or code != int(code):
            raise ValueError("Unknown temporary crop code")
    temporary_pairs = {(k[0], k[2]) for k, kind in zip(source_keys[1], cc.s03_cropsType, strict=True) if kind == 1}
    if any(k not in temporary_pairs for k in source_keys[2]):
        raise ValueError("Harvest record lacks temporary household-crop parent")
    for frame, column, module in ((hh, "s01b_harvestedCrops__id", MODULES[2]),
                                  (ii, "s03c_inputType__id", MODULES[3])):
        allowed = {int(k) for k in reference[module]["value_labels"][column]}
        if not frame[column].isin(allowed).all():
            raise ValueError("Unknown roster category")

    with sqlite3.connect(":memory:") as db:
        # Numeric raw responses, not Python category counts, feed independent SQL.
        for table, frame in zip(("plots", "crops", "harvest", "inputs"), normalized, strict=True):
            frame.to_sql(table, db, index=False)
        db.executescript(sql_text())

        def tally(frame: pd.DataFrame, table: str, condition: str) -> int:
            n = len(frame)
            if db.execute(f"SELECT COUNT(*) FROM {table} WHERE {condition}").fetchone()[0] != n:
                raise ValueError("Eligibility SQL/Python disagreement")
            return n

        def categorical(frame: pd.DataFrame, table: str, column: str, labels: dict,
                        condition: str = "1") -> dict:
            allowed = {int(k): v for k, v in labels.items()}
            codes = sorted(allowed)
            def category(v):
                if is_missing(v):
                    return "missing"
                return str(int(v)) if v in allowed else "invalid"
            counts = Counter(category(v) for v in frame[column])
            sql = (f'SELECT CASE WHEN "{column}" IS NULL THEN \'missing\' '
                   f'WHEN "{column}" IN ({",".join(map(str, codes))}) THEN '
                   f'CAST(CAST("{column}" AS INTEGER) AS TEXT) ELSE \'invalid\' END category, '
                   f'COUNT(*) FROM {table} WHERE {condition} GROUP BY category')
            if dict(counts) != dict(db.execute(sql)):
                raise ValueError("Category SQL/Python disagreement")
            n = tally(frame, table, condition)
            valid = sum(counts[str(k)] for k in codes)
            return {"eligible": n, "valid": valid, "missing": counts["missing"],
                    "invalid": counts["invalid"], "rows": [
                        {"code": k, "label": allowed[k], "count": counts[str(k)],
                         "share": counts[str(k)]/valid if valid else None} for k in codes]}

        def field(frame, table, column, module, condition="1"):
            return categorical(frame, table, column, reference[module]["value_labels"][column], condition)

        land = {name: field(pp, "plots", column, MODULES[0]) for name, column in
                (("tenure", "s02_q04"), ("transport", "s02_q05"))}
        travel_mask = pp.s02_q05.isin(range(1, 6))
        land["travel"] = field(pp[travel_mask], "plots", "s02_q06", MODULES[0], "s02_q05 IN (1,2,3,4,5)")
        land["on_dwelling"] = tally(pp[pp.s02_q05.eq(6)], "plots", "s02_q05=6")
        land["unknown_transport"] = len(pp)-int(travel_mask.sum())-land["on_dwelling"]
        land["outside_travel_answers"] = tally(pp[~travel_mask & pp.s02_q06.notna()], "plots",
            "(s02_q05 IS NULL OR s02_q05 NOT IN (1,2,3,4,5)) AND s02_q06 IS NOT NULL")

        temporary = cc.s03_cropsType.eq(1)
        a, v = cc.s01a_q07.notna(), cc.s01h_q08.notna()
        difficulties = {"temporary_records": tally(cc[temporary], "crops", "s03_cropsType=1"),
            "excluded_permanent": tally(cc[~temporary], "crops", "s03_cropsType=2"),
            "unassigned": tally(cc[temporary & ~a & ~v], "crops", "s03_cropsType=1 AND s01a_q07 IS NULL AND s01h_q08 IS NULL"),
            "ambiguous": tally(cc[temporary & a & v], "crops", "s03_cropsType=1 AND s01a_q07 IS NOT NULL AND s01h_q08 IS NOT NULL"),
            "branches": []}
        for index, (name, any_field, complete_field, shock_field, no_prefix, shock_prefix) in enumerate(BRANCHES):
            other = BRANCHES[1-index][1]
            mask = temporary & cc[any_field].notna() & cc[other].isna()
            where = f"s03_cropsType=1 AND {any_field} IS NOT NULL AND {other} IS NULL"
            branch = {"name": name, "harvest": field(cc[mask], "crops", any_field, MODULES[1], where)}
            for title, prefix, submask, subwhere in (
                ("no_harvest_reasons", no_prefix, mask & cc[any_field].eq(2), where+f" AND {any_field}=2"),
                ("shock_reasons", shock_prefix, mask & cc[any_field].eq(1) & cc[complete_field].eq(2) & cc[shock_field].eq(1),
                 where+f" AND {any_field}=1 AND {complete_field}=2 AND {shock_field}=1")):
                branch[title] = [{"field": col, "label": reference[MODULES[1]]["labels"][col].split(":")[-1].strip(),
                                  **field(cc[submask], "crops", col, MODULES[1], subwhere)}
                                 for col in reference[MODULES[1]]["labels"] if col.startswith(prefix)]
            shock_mask = mask & cc[any_field].eq(1) & cc[complete_field].eq(2)
            shock_where = where+f" AND {any_field}=1 AND {complete_field}=2"
            branch["shocks"] = field(cc[shock_mask], "crops", shock_field, MODULES[1], shock_where)
            branch["completion"] = field(cc[mask & cc[any_field].eq(1)], "crops", complete_field, MODULES[1], where+f" AND {any_field}=1")
            branch["outside_shock_answers"] = tally(cc[mask & ~shock_mask & cc[shock_field].notna()], "crops",
                where+f" AND ({any_field}!=1 OR {complete_field} IS NULL OR {complete_field}!=2) AND {shock_field} IS NOT NULL")
            difficulties["branches"].append(branch)

        destinations = {name: field(hh, "harvest", col, MODULES[2]) for name, col in
                        (("sales", "s01b_q02"), ("storage", "s01b_q20"), ("losses", "s01b_q11"))}
        destinations["crops"] = []
        for code in sorted(hh.s01b_harvestedCrops__id.unique()):
            selected = hh.s01b_harvestedCrops__id.eq(code)
            destinations["crops"].append({"code": int(code), "label": reference[MODULES[2]]["value_labels"]["s01b_harvestedCrops__id"][str(int(code))],
                **{name: field(hh[selected], "harvest", col, MODULES[2], f"s01b_harvestedCrops__id={int(code)}") for name, col in
                   (("sales", "s01b_q02"), ("storage", "s01b_q20"), ("losses", "s01b_q11"))}})
        complete = hh.s01b_q02.isin([1, 2]) & hh.s01b_q20.isin([1, 2])
        joint = Counter(tuple(r) for r in hh.loc[complete, ["s01b_q02", "s01b_q20"]].itertuples(index=False, name=None))
        sql_joint = {(a, b): n for a, b, n in db.execute("SELECT s01b_q02,s01b_q20,COUNT(*) FROM destination_complete GROUP BY s01b_q02,s01b_q20")}
        if dict(joint) != sql_joint:
            raise ValueError("Overlap SQL/Python disagreement")
        destinations["overlap"] = {"valid": int(complete.sum()), "excluded": len(hh)-int(complete.sum()),
            "cells": [{"sales": a, "storage": b, "count": joint[(a, b)]} for a in (1, 2) for b in (1, 2)]}

        input_rows = []
        for code in sorted(ii.s03c_inputType__id.unique()):
            selected = ii[ii.s03c_inputType__id.eq(code)]
            def status(v):
                if is_missing(v):
                    return "Missing"
                return "Invalid" if not math.isfinite(v) or v < 0 else "Zero" if v == 0 else "Positive"
            counts = Counter(status(v) for v in selected.s03c_q01)
            sql_counts = dict(db.execute("SELECT quantity_status,COUNT(*) FROM input_quality WHERE s03c_inputType__id=? GROUP BY quantity_status", (float(code),)))
            if dict(counts) != sql_counts:
                raise ValueError("Quantity SQL/Python disagreement")
            n = tally(selected, "inputs", f"s03c_inputType__id={int(code)}")
            input_rows.append({"code": int(code), "label": reference[MODULES[3]]["value_labels"]["s03c_inputType__id"][str(int(code))],
                "records": n, "statuses": [{"label": s, "count": counts[s], "share": counts[s]/n if n else None}
                                          for s in ("Positive", "Zero", "Missing", "Invalid")]})
    return {"counts": {"households": len(hh_keys), "plots": len(pp), "crops": len(cc), "harvest": len(hh), "inputs": len(ii)},
            "land": land, "difficulties": difficulties, "destinations": destinations, "inputs": input_rows}


def run(archive_path: Path, output: Path) -> None:
    root = Path.cwd().resolve()
    if not output.resolve().is_relative_to(root / "reports/private"):
        raise ValueError("Output must be private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Unreviewed archive")
    tables, reference = [], metadata()
    with zipfile.ZipFile(archive_path) as archive:
        households, _ = read_selected(archive, "1_households.dta", ("hhid", "mainAgSeason", "referenceAgYear"))
        check_period(households)
        for module in MODULES:
            frame, info = read_selected(archive, module, tuple(reference[module]["labels"]))
            if info["selected_columns"] != reference[module]["labels"]:
                raise ValueError("Field labels changed")
            with archive.open(module) as stream, pd.io.stata.StataReader(stream) as reader:
                labels = {k: {str(c): v for c, v in values.items()} for k, values in reader.value_labels().items()}
                if any(labels.get(k) != v for k, v in reference[module]["value_labels"].items()):
                    raise ValueError("Value labels changed")
            tables.append(frame)
    result = {"version": "1.0", "source_sha256": digest, "provenance": {
        "model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sql_sha256": hashlib.sha256(sql_text().encode()).hexdigest(),
        "labels_sha256": hashlib.sha256(files("agrisight").joinpath("reporting/conditions_labels_v1.json").read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256((root/"docs/FARMING_CONDITIONS_CONTRACT.md").read_bytes()).hexdigest(),
        "lock_sha256": hashlib.sha256((root/"requirements/e1.lock").read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "pandas": pd.__version__, "sqlite": sqlite3.sqlite_version},
        **calculate(households, *tables)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8", newline="\n")
    print("FC1 checked aggregates saved in private reports")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
