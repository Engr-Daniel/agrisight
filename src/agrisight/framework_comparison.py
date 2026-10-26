"""M0-05 optional framework comparison on the same synthetic dataframe.

Install extra packages first; no real respondent data are used.
"""
from __future__ import annotations

import json
from importlib.metadata import version

from agrisight.quality_baseline import example_inputs


def compare() -> dict[str, object]:
    import pandas as pd
    import pandera.pandas as pa
    import great_expectations as gx

    good, bad = example_inputs()
    # Nonidentifying synthetic records only.
    columns = ["role_id", "person_id", "kind", "status", "complete"]

    # Pandera: schema and row-integrity contract, with eager combined errors.
    schema = pa.DataFrameSchema(
        {
            "role_id": pa.Column(str, pa.Check(lambda s: s.str.strip().ne("").all()), unique=True),
            "person_id": pa.Column(str, pa.Check(lambda s: s.str.strip().ne("").all())),
            "kind": pa.Column(str, pa.Check.isin(["farmer", "processor"])),
            "status": pa.Column(str, pa.Check.isin(["accepted", "pending", "rejected"])),
            "complete": pa.Column(bool),
        },
        strict=True,
        coerce=False,
    )
    pandera_results = {}
    for label, rows in [("valid", good), ("invalid", bad)]:
        try:
            schema.validate(pd.DataFrame(rows, columns=columns), lazy=True)
            pandera_results[label] = True
        except pa.errors.SchemaErrors:
            pandera_results[label] = False

    # GX: compare the shared column-level expectations. Cross-column strict
    # typing and duplicate-row semantics are separately implemented above,
    # and must not be misrepresented as full parity in this first experiment.
    gx_results = {}
    for label, rows in [("valid", good), ("invalid", bad)]:
        context = gx.get_context(mode="ephemeral")
        source = context.data_sources.add_pandas(name=f"source_{label}")
        asset = source.add_dataframe_asset(name=f"asset_{label}")
        definition = asset.add_batch_definition_whole_dataframe(name=f"batch_{label}")
        batch = definition.get_batch(batch_parameters={"dataframe": pd.DataFrame(rows, columns=columns)})
        expectations = [
            gx.expectations.ExpectColumnValuesToNotBeNull(column="person_id"),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="kind", value_set=["farmer", "processor"]
            ),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="status", value_set=["accepted", "pending", "rejected"]
            ),
            gx.expectations.ExpectColumnValuesToBeUnique(column="role_id"),
        ]
        gx_results[label] = all(batch.validate(e).success for e in expectations)

    outcome = {
        "versions": {
            "pandas": version("pandas"),
            "pandera": version("pandera"),
            "great_expectations": version("great_expectations"),
        },
        "pandera": pandera_results,
        "gx_core_partial_contract": gx_results,
        "note": "Partial GX check: empty-string and strict-boolean rules not yet included.",
    }
    return outcome


def main() -> None:
    outcome = compare()
    print(json.dumps(outcome, indent=2))
    assert outcome["pandera"] == {"valid": True, "invalid": False}
    assert outcome["gx_core_partial_contract"] == {"valid": True, "invalid": False}


if __name__ == "__main__":
    main()
