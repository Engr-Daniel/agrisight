"""M0-05: comparable synthetic validation cases in Pandera and GX Core."""
from __future__ import annotations

import json
from importlib.metadata import version

COLUMNS = ("role_id", "person_id", "kind", "status", "complete")


def cases() -> dict[str, list[dict]]:
    base = [
        {"role_id": "R1", "person_id": "P1", "kind": "farmer",
         "status": "accepted", "complete": True},
        {"role_id": "R2", "person_id": "P1", "kind": "processor",
         "status": "accepted", "complete": False},
    ]
    scenarios = {"valid": base}
    mutations = {
        "empty_person_id": ("person_id", ""),
        "empty_role_id": ("role_id", ""),
        "invalid_kind": ("kind", "dealer"),
        "invalid_status": ("status", "unknown"),
        "invalid_boolean": ("complete", 1),
        "duplicate_role_id": ("role_id", "R1"),
    }
    for name, (column, value) in mutations.items():
        rows = [dict(r) for r in base]
        rows[1][column] = value
        scenarios[name] = rows
    return scenarios


def compare() -> dict[str, object]:
    import great_expectations as gx
    import pandas as pd
    import pandera.pandas as pa

    schema = pa.DataFrameSchema(
        {
            "role_id": pa.Column(
                str, pa.Check.str_matches(r"^\S(?:.*\S)?$"), unique=True
            ),
            "person_id": pa.Column(
                str, pa.Check.str_matches(r"^\S(?:.*\S)?$")
            ),
            "kind": pa.Column(str, pa.Check.isin(["farmer", "processor"])),
            "status": pa.Column(
                str, pa.Check.isin(["accepted", "pending", "rejected"])
            ),
            "complete": pa.Column(bool, coerce=False),
        },
        strict=True,
        coerce=False,
    )

    results = {}
    for name, rows in cases().items():
        frame = pd.DataFrame(rows, columns=list(COLUMNS))
        try:
            schema.validate(frame, lazy=True)
            pandera_valid = True
        except (pa.errors.SchemaError, pa.errors.SchemaErrors):
            pandera_valid = False

        context = gx.get_context(mode="ephemeral")
        source = context.data_sources.add_pandas(name=f"source_{name}")
        asset = source.add_dataframe_asset(name=f"asset_{name}")
        definition = asset.add_batch_definition_whole_dataframe(name=f"batch_{name}")
        batch = definition.get_batch(batch_parameters={"dataframe": frame})
        expectations = [
            gx.expectations.ExpectColumnValuesToMatchRegex(
                column="role_id", regex=r"^\S(?:.*\S)?$"
            ),
            gx.expectations.ExpectColumnValuesToMatchRegex(
                column="person_id", regex=r"^\S(?:.*\S)?$"
            ),
            gx.expectations.ExpectColumnValuesToBeUnique(column="role_id"),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="kind", value_set=["farmer", "processor"]
            ),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="status", value_set=["accepted", "pending", "rejected"]
            ),
            gx.expectations.ExpectColumnValuesToBeOfType(
                column="complete", type_="bool"
            ),
        ]
        gx_valid = all(batch.validate(e).success for e in expectations)
        results[name] = {
            "expected": name == "valid",
            "pandera": pandera_valid,
            "gx": gx_valid,
        }
    return {
        "versions": {
            "pandas": version("pandas"),
            "pandera": version("pandera"),
            "great_expectations": version("great_expectations"),
        },
        "cases": results,
        "scope": "Shared synthetic cases only; no timing or production benchmark.",
    }


def main() -> None:
    outcome = compare()
    print(json.dumps(outcome, indent=2))
    for name, result in outcome["cases"].items():
        assert result["pandera"] == result["expected"], name
        assert result["gx"] == result["expected"], name


if __name__ == "__main__":
    main()
