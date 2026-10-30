"""State-level sample coverage, never geographic population estimates."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import zipfile
from collections import Counter
from importlib.resources import files
from pathlib import Path

import pandas as pd

from agrisight.e1_profile import ARCHIVE_SHA256, identifier, read_selected

STATE_NAMES = ("SOKOTO", "ZAMFARA", "KATSINA", "JIGAWA", "YOBE", "BORNO", "ADAMAWA", "GOMBE",
               "BAUCHI", "KANO", "KADUNA", "KEBBI", "NIGER", "FCT", "NASARAWA", "PLATEAU",
               "TARABA", "BENUE", "KOGI", "KWARA", "OYO", "OSUN", "EKITI", "ONDO", "EDO",
               "ANAMBRA", "ENUGU", "EBONYI", "CROSS RIVER", "AKWA IBOM", "ABIA", "IMO",
               "RIVERS", "BAYELSA", "DELTA", "LAGOS", "OGUN")


def calculate(frame: pd.DataFrame) -> dict:
    if not frame.columns.is_unique or not {"hhid", "state_id"}.issubset(frame.columns):
        raise ValueError("Missing or duplicated coverage columns")
    rows, keys = [], set()
    for household, state in frame[["hhid", "state_id"]].itertuples(index=False, name=None):
        key = identifier(household)
        if key is None or key in keys or isinstance(state, bool) or pd.isna(state) or state not in range(1, 38):
            raise ValueError("Invalid household key or state code")
        keys.add(key)
        rows.append((key, int(state)))
    counts = Counter(row[1] for row in rows)
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE households(id TEXT PRIMARY KEY, state INTEGER NOT NULL)")
        db.executemany("INSERT INTO households VALUES(?,?)", rows)
        independent = dict(db.execute("SELECT state,COUNT(*) FROM households GROUP BY state"))
    if dict(counts) != independent:
        raise ValueError("Coverage SQL/Python mismatch")
    return {"total": len(rows), "states": [
        {"code": code, "name": name, "households": counts[code]}
        for code, name in enumerate(STATE_NAMES, 1)]}


def run(archive_path: Path, output: Path) -> None:
    root = Path.cwd().resolve()
    if not output.resolve().is_relative_to(root / "reports/private"):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Unreviewed source archive")
    with zipfile.ZipFile(archive_path) as archive:
        frame, metadata = read_selected(archive, "1_households.dta", ("hhid", "state_id"))
        if metadata["selected_columns"]["state_id"] != "STATE":
            raise ValueError("State field label changed")
        with archive.open("1_households.dta") as stream, pd.io.stata.StataReader(stream) as reader:
            labels = reader.value_labels().get("state_id")
            if labels != dict(enumerate(STATE_NAMES, 1)):
                raise ValueError("State code labels changed")
    result = {"version": "1.0", "source_sha256": digest,
              "provenance": {"model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "contract_sha256": hashlib.sha256((root / "docs/GEOGRAPHIC_COVERAGE_CONTRACT.md")
                                                     .read_bytes()).hexdigest(),
                  "boundary_sha256": hashlib.sha256(files("agrisight").joinpath(
                      "reporting/nigeria_adm1_v1.json").read_bytes()).hexdigest(),
                  "python": sys.version.split()[0], "pandas": pd.__version__,
                  "sqlite": sqlite3.sqlite_version}, **calculate(frame)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Coverage aggregates saved under ignored reports/private")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.archive, arguments.output)
