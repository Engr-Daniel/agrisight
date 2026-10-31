"""SS1: temporary household-crop seed channels; variety interpretation is gated."""

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
from agrisight.e1_profile import ARCHIVE_SHA256, is_missing, read_selected, response
from agrisight.nass01 import check_period

FIELDS = tuple(f"s04_q03a__{i}" for i in range(1, 6))
NAMES = ("Produced on the holding", "Community exchange", "Purchased from local market",
         "Purchased from seed company", "Received as a donation")
PERIODS = {1: "2022/2023 RAINY SEASON (APRIL 2022-OCT 2022)", 2: "2022/2023 AGRICULTURAL SEASON"}


def metadata() -> dict:
    return json.loads(files("agrisight").joinpath("reporting/seed_labels_v1.json").read_bytes())


def sql_text() -> str:
    return files("agrisight").joinpath("sql/seed_sources.sql").read_text(encoding="utf-8")


def binary(value: object) -> str:
    if is_missing(value):
        return "missing"
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError("Expected numeric binary seed response")
    return "yes" if value == 1 else "no" if value == 0 else "invalid"


def calculate(households: pd.DataFrame, seeds: pd.DataFrame) -> dict:
    hh_keys = keys(households, ("hhid",))
    seed_keys = keys(seeds, ("hhid", "s04_cropRoster__id"))
    required = ("hhid", "s04_cropRoster__id", "s04_cropsType", "s04_reference", *FIELDS)
    if not set(required).issubset(seeds.columns) or "s00_q15a" not in households:
        raise ValueError("Missing seed/household fields")
    known = {k[0] for k in hh_keys}
    yes_households = {k[0] for k, v in zip(hh_keys, households.s00_q15a, strict=True) if response(v) == "yes"}
    labels = metadata()["value_labels"]["s04_cropRoster__id"]
    rows = []
    for key, raw in zip(seed_keys, seeds[list(required)].itertuples(index=False, name=None), strict=True):
        _, code, kind, period, *values = raw
        if key[0] not in known:
            raise ValueError("Orphan seed household")
        if (not isinstance(code, Real) or isinstance(code, bool) or not math.isfinite(code)
                or str(int(code)) not in labels or code != int(code)
                or not isinstance(kind, Real) or isinstance(kind, bool) or kind not in PERIODS):
            raise ValueError("Unknown crop code/type")
        if period != PERIODS[kind]:
            raise ValueError("Seed reference period differs")
        rows.append((*key, int(kind), *(binary(v) for v in values)))
    eligible = [r for r in rows if r[2] == 1]
    represented = {r[0] for r in eligible}
    counters = [Counter(r[3+i] for r in eligible) for i in range(5)]
    combinations = Counter(sum((v == "yes") << i for i, v in enumerate(r[3:]))
                           for r in eligible if all(v in ("yes", "no") for v in r[3:]))
    c = {"household_records": len(hh_keys), "seed_rows": len(rows), "eligible_records": len(eligible),
         "excluded_permanent_records": len(rows)-len(eligible), "represented_households": len(represented),
         "crop_yes_without_temporary_seed_record": len(yes_households-represented),
         "temporary_seed_households_without_crop_yes": len(represented-yes_households)}
    valid_condition = " AND ".join(f"s{i} IN ('yes','no')" for i in range(5))
    mask = "+".join(f"(s{i}='yes')*{1 << i}" for i in range(5))
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE households(hh TEXT PRIMARY KEY,presence TEXT)")
        db.executemany("INSERT INTO households VALUES(?,?)", [(k[0], response(v)) for k, v in zip(hh_keys, households.s00_q15a, strict=True)])
        db.execute("CREATE TABLE seeds(hh TEXT,crop TEXT,kind INTEGER,s0 TEXT,s1 TEXT,s2 TEXT,s3 TEXT,s4 TEXT,PRIMARY KEY(hh,crop))")
        db.executemany("INSERT INTO seeds VALUES(?,?,?,?,?,?,?,?)", rows)
        sql_counts = [{} for _ in range(5)]
        for index, value, n in db.execute(sql_text()):
            sql_counts[index][value] = n
        sql_combos = dict(db.execute(f"SELECT {mask},COUNT(*) FROM seeds WHERE kind=1 AND {valid_condition} GROUP BY {mask}"))
        sql_summary = db.execute("SELECT (SELECT COUNT(*) FROM households),COUNT(*),COALESCE(SUM(kind=1),0),"
            "COALESCE(SUM(kind=2),0),COUNT(DISTINCT CASE WHEN kind=1 THEN hh END) FROM seeds").fetchone()
        sql_gap = db.execute("SELECT COUNT(*) FROM households WHERE presence='yes' AND hh NOT IN (SELECT hh FROM seeds WHERE kind=1)").fetchone()[0]
        sql_other = db.execute("SELECT COUNT(DISTINCT s.hh) FROM seeds s JOIN households h ON s.hh=h.hh WHERE s.kind=1 AND h.presence!='yes'").fetchone()[0]
    if ([dict(v) for v in counters] != sql_counts or dict(combinations) != sql_combos
            or tuple(c.values()) != (*sql_summary, sql_gap, sql_other)):
        raise ValueError("Seed SQL/Python disagreement")
    sources = []
    for index, counts in enumerate(counters):
        valid = counts["yes"]+counts["no"]
        sources.append({"id": index+1, "label": NAMES[index], "yes": counts["yes"], "no": counts["no"],
            "missing": counts["missing"], "invalid": counts["invalid"], "denominator": valid,
            "share": counts["yes"]/valid if valid else None})
    complete = sum(combinations.values())
    return {"counts": c, "sources": sources, "combinations": {"denominator": complete,
        "excluded": len(eligible)-complete, "rows": [{"mask": mask, "records": n, "share": n/complete}
            for mask, n in sorted(combinations.items())]}, "variety_status": "interpretation_not_verified"}


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
        fields = ("hhid", "s04_cropRoster__id", "s04_cropsType", "s04_reference", *FIELDS)
        seeds, labels = read_selected(archive, "8_Seed_use_mainSeason.dta", fields)
        reference = metadata()
        if any(labels["selected_columns"][k] != reference["labels"][k] for k in fields if k != "hhid"):
            raise ValueError("Seed field labels changed")
        with archive.open("8_Seed_use_mainSeason.dta") as stream, pd.io.stata.StataReader(stream) as reader:
            value_labels = {k: {str(c): v for c, v in values.items()} for k, values in reader.value_labels().items()}
            if any(value_labels.get(k) != v for k, v in reference["value_labels"].items()):
                raise ValueError("Seed category labels changed")
    provenance = {"model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sql_sha256": hashlib.sha256(sql_text().encode()).hexdigest(),
        "contract_sha256": hashlib.sha256((root / "docs/SEED_SOURCE_CONTRACT.md").read_bytes()).hexdigest(),
        "labels_sha256": hashlib.sha256(files("agrisight").joinpath("reporting/seed_labels_v1.json").read_bytes()).hexdigest(),
        "lock_sha256": hashlib.sha256((root / "requirements/e1.lock").read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "pandas": pd.__version__, "sqlite": sqlite3.sqlite_version}
    result = {"version": "1.0", "source_sha256": digest, "provenance": provenance, **calculate(hh, seeds)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Seed-source aggregates saved under ignored reports/private")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
