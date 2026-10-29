"""M1 source suitability extension; aggregate-only local outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import zipfile
from numbers import Real
from pathlib import Path

import pandas as pd

from agrisight.e1_profile import (
    ARCHIVE_SHA256,
    identifier,
    is_missing,
    profile_frames,
    read_selected,
    response,
)

ACTIVITIES = ("s00_q15a", "s00_q15b", "s00_q16", "s00_q17", "s00_q18")
PERIODS = ("referenceAgYear", "mainAgSeason", "minorAgSeason")


def numeric_summary(values: pd.Series) -> dict[str, int]:
    result = dict.fromkeys(("missing", "nonfinite", "negative", "zero", "positive"), 0)
    for value in values:
        if is_missing(value):
            result["missing"] += 1
        elif not isinstance(value, Real) or isinstance(value, bool):
            raise TypeError("Expected numeric quantities, no source values logged")
        elif not math.isfinite(value):
            result["nonfinite"] += 1
        else:
            result["negative" if value < 0 else "zero" if value == 0 else "positive"] += 1
    return result


def skip_checks(plots: pd.DataFrame) -> dict[str, int]:
    """Questionnaire q7=no skips method/source; valid method/source codes from labels."""
    presence = plots.s02_q07.map(response)
    result = {}
    for field, allowed in (("s02_q08", set(range(1, 9)) | {99}),
                           ("s02_q09", set(range(1, 7)) | {99})):
        missing = plots[field].map(is_missing)
        valid = plots[field].map(
            lambda value, codes=allowed: False if is_missing(value) else value in codes
        )
        result[f"{field}_missing_when_yes"] = int(((presence == "yes") & missing).sum())
        result[f"{field}_other_when_yes"] = int(
            ((presence == "yes") & ~missing & ~valid).sum()
        )
        result[f"{field}_populated_when_no"] = int(((presence == "no") & ~missing).sum())
    return result


def input_checks(inputs: pd.DataFrame, households: pd.DataFrame) -> dict:
    keys = pd.DataFrame({"hhid": inputs.hhid.map(identifier),
                         "input_type": inputs.s03c_inputType__id.map(identifier)})
    complete = keys.dropna()
    known = set(households.hhid.map(identifier).dropna())
    return {
        "rows": len(keys), "missing_key_rows": len(keys) - len(complete),
        "distinct_complete_keys": len(complete.drop_duplicates()),
        "duplicate_excess": len(complete) - len(complete.drop_duplicates()),
        "orphan_household_rows": int((keys.hhid.notna() & ~keys.hhid.isin(known)).sum()),
        "quantity": numeric_summary(inputs.s03c_q01),
    }


def schema_inventory(archive: zipfile.ZipFile) -> dict:
    """Inspect metadata for all files, retaining no variable contents."""
    inventory = {}
    pattern = re.compile(r"\b(psu|strat\w*|cluster\w*|replic\w*|bootstrap|jackknife|"
                         r"enumeration|ea)\b", re.IGNORECASE)
    for name in archive.namelist():
        if not name.endswith(".dta"):
            continue
        with archive.open(name) as stream, pd.io.stata.StataReader(stream) as reader:
            labels = reader.variable_labels()
            inventory[name] = {
                "variables": len(labels),
                "design_candidates": {key: value for key, value in labels.items()
                                      if pattern.search(key.replace("_", " ") + " " + value)},
            }
    return inventory


def run(archive_path: Path, output: Path) -> None:
    if not output.resolve().is_relative_to((Path.cwd() / "reports/private").resolve()):
        raise ValueError("Output must be inside reports/private")
    with archive_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError("Archive hash mismatch")
    with zipfile.ZipFile(archive_path) as archive:
        inventory = schema_inventory(archive)
        hh, _ = read_selected(archive, "1_households.dta",
                              ("hhid", "final_weight", *ACTIVITIES, *PERIODS))
        pp, _ = read_selected(archive, "3_Plot_mainSeason.dta",
                              ("hhid", "s02_plotRoster__id", "final_weight", "s02_q07",
                               "s02_q08", "s02_q09", "s02_q16a"))
        dry, _ = read_selected(archive, "10_Plots_drySeason.dta",
                               ("hhid", "s02_plotRoster_ds__id", "s02_q07_ds", "final_weight"))
        inputs, _ = read_selected(archive, "9_Input_use_mainSeason.dta",
                                  ("hhid", "s03c_inputType__id", "s03c_q01"))
    activity_counts = {
        field: {code: int(hh[field].map(response).eq(code).sum())
                for code in ("yes", "no", "missing", "other")} for field in ACTIVITIES
    }
    # Only allow-listed agricultural reference fields; no interview dates or free text.
    periods = {}
    for field in PERIODS:
        values = sorted({str(v) for v in hh[field] if not is_missing(v)})
        periods[field] = {"missing": int(hh[field].map(is_missing).sum()),
                          "distinct_nonmissing": len(values), "values": values}
    if any(len(item["values"]) > 10 for item in periods.values()):
        raise ValueError("Unexpectedly varied reference fields; inspect privately")
    dry = dry.rename(columns={"s02_plotRoster_ds__id": "s02_plotRoster__id",
                              "s02_q07_ds": "s02_q07"})
    result = {
        "protocol": "E1.2", "sha256": digest, "scope": "Sample suitability, no inference",
        "schema_inventory": inventory, "activity_codes": activity_counts,
        "reference_fields": periods, "main_plot_key_checks": profile_frames(hh, pp),
        "dry_plot_key_checks": profile_frames(hh, dry),
        "irrigation_skip_checks": skip_checks(pp),
        "plot_area": numeric_summary(pp.s02_q16a),
        "main_season_inputs": input_checks(inputs, hh),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.archive, args.output)
    print("E1.2 aggregate suitability output saved under reports/private.")


if __name__ == "__main__":
    main()
