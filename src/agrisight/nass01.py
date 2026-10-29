"""NASS-01: independently reconciled, unweighted observed-sample indicator."""

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

MODEL_VERSION = "1.0"
EXPECTED_PERIOD = "2022/2023 RAINY SEASON (APRIL 2022-OCT 2022)"
EXPECTED_YEAR = "2022/2023 AGRICULTURAL YEAR"
REQUIRED = ("hhid", "s00_q15a")
COUNTS = ("input_rows", "numerator", "denominator", "no_count", "missing_count",
          "invalid_count", "excluded_count")
RATES = ("proportion", "percentage")
TOLERANCE = 1e-12


def sql_model() -> str:
    return files("agrisight").joinpath("sql/nass01.sql").read_text(encoding="utf-8")


def stage(frame: pd.DataFrame) -> list[tuple[str, float | None]]:
    """Preserve one row per household; reject ambiguous keys rather than deduplicate."""
    if not frame.columns.is_unique or not set(REQUIRED).issubset(frame.columns):
        raise ValueError("Required columns missing or duplicated")
    rows = []
    seen = set()
    for raw_key, code in frame[list(REQUIRED)].itertuples(index=False, name=None):
        key = identifier(raw_key)
        if key is None or key in seen:
            raise ValueError("Missing or duplicate household key; no records dropped")
        seen.add(key)
        if is_missing(code):
            numeric = None
        elif isinstance(code, Real) and not isinstance(code, bool):
            # Preserve invalid numeric responses as invalid, including infinity.
            numeric = float(code)
        else:
            raise TypeError("Expected numeric activity codes, not coerced text/booleans")
        rows.append((key, numeric))
    return rows


def python_indicator(frame: pd.DataFrame) -> dict:
    """Reference aggregation directly from selected responses, not SQL statuses."""
    yes = no = missing = invalid = 0
    for value in frame.s00_q15a:
        if is_missing(value):
            missing += 1
        elif value == 1:
            yes += 1
        elif value == 2:
            no += 1
        else:
            invalid += 1
    denominator = yes + no
    return {
        "input_rows": len(frame), "numerator": yes, "denominator": denominator,
        "no_count": no, "missing_count": missing, "invalid_count": invalid,
        "excluded_count": missing + invalid,
        "proportion": yes / denominator if denominator else None,
        "percentage": 100 * yes / denominator if denominator else None,
    }


def sql_indicator(rows: list[tuple[str, float | None]]) -> dict:
    """Constrained staging → eligibility view → single-row indicator mart."""
    with sqlite3.connect(":memory:") as db:
        db.row_factory = sqlite3.Row
        db.executescript(sql_model())
        db.executemany("INSERT INTO stg_nass_households VALUES (?,?)", rows)
        return dict(db.execute("SELECT * FROM mart_nass01").fetchone())


def reconcile(python: dict, sql: dict) -> None:
    for name in COUNTS:
        if python[name] != sql[name]:
            raise ValueError("Integer reconciliation failed; no indicator output")
    for name in RATES:
        left, right = python[name], sql[name]
        if left is None or right is None:
            matched = left is None and right is None
        else:
            matched = math.isclose(left, right, rel_tol=0, abs_tol=TOLERANCE)
        if not matched:
            raise ValueError("Rate reconciliation failed; no indicator output")


def calculate(frame: pd.DataFrame) -> dict:
    rows = stage(frame)
    python, sql = python_indicator(frame), sql_indicator(rows)
    reconcile(python, sql)
    return {
        "counts_and_rates": sql,
        "reconciliation": {"integer_counts": "exact match", "rates": "within tolerance",
                           "absolute_tolerance": TOLERANCE},
    }


def check_period(frame: pd.DataFrame) -> None:
    for field, expected in (("mainAgSeason", EXPECTED_PERIOD),
                            ("referenceAgYear", EXPECTED_YEAR)):
        if field not in frame or any(not isinstance(value, str) or value != expected
                                     for value in frame[field]):
            raise ValueError("Reference period differs from the NASS-01 contract")


def run(archive_path: Path, output: Path) -> None:
    private = (Path.cwd() / "reports/private").resolve()
    if not output.resolve().is_relative_to(private):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Archive hash differs from the acquired input contract")
    with zipfile.ZipFile(archive_path) as archive:
        frame, _ = read_selected(archive, "1_households.dta",
                                  (*REQUIRED, "mainAgSeason", "referenceAgYear"))
    check_period(frame)
    result = {
        "indicator": "NASS-01", "contract_version": "1.0", "model_version": MODEL_VERSION,
        "source": {"archive_sha256": digest, "member": "1_households.dta",
                   "origin": "owner-supplied NBS survey archive", "acquired": "2026-10-29"},
        "definition": {
            "grain": "one released agricultural-household record per unique complete hhid",
            "numerator": "households with s00_q15a=1",
            "denominator": "households with s00_q15a in (1,2)",
            "period": "April-October 2022", "reference_year": "2022/2023 agricultural year",
            "geographic_scope": "pooled observed sample only",
            "weighting": "unweighted", "missing_invalid": "excluded, separately counted",
            "zero_denominator": "undefined/null", "uncertainty": "not estimated",
            "interpretation_limit": "Not a national/domain estimate or current prevalence",
        },
        "provenance": {
            "sql_sha256": hashlib.sha256(sql_model().encode("utf-8")).hexdigest(),
            "python_model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_lock_sha256": hashlib.sha256(
                Path("requirements/e1.lock").read_bytes()
            ).hexdigest(),
            "pandas": pd.__version__, "python": sys.version.split()[0],
            "sqlite": sqlite3.sqlite_version,
        },
        **calculate(frame),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("NASS-01 aggregate indicator saved under ignored reports/private.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)


if __name__ == "__main__":
    main()
