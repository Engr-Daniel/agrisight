"""AppTest UI checks use labelled TEST FIXTURE aggregates, never restricted inputs."""

import json
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest
from test_reporting_adapter import fixture_data, m, metrics, write_fixture

from agrisight import reporting_adapter
from agrisight.reporting_ui import (
    COUNT_LABELS,
    build_time,
    decimal,
    integer,
    percentage,
)

ROOT = Path(__file__).resolve().parents[1]


def ui_data():
    data = fixture_data()
    # Hand-defined aggregate outcomes exercise positive/error and undefined rates;
    # these are UI fixtures, not claimed results of the M3 generator or detector.
    for run in data["m3_04_evaluation.json"]["runs"]:
        if run["configuration"] != "Mixed":
            continue
        run.update(events=4, people=2, intended_roles=3)
        for baseline in ("B0", "B1"):
            result = metrics(4)
            result["same_person"] = m(6, tp=1 if baseline == "B0" else 3, fp=1,
                                      fn=2 if baseline == "B0" else 0)
            result["duplicate_role"] = m(6, tp=0 if baseline == "B0" else 1, fp=1,
                                         fn=1 if baseline == "B0" else 0)
            result["quality_by_rule"]["missing_contact"] = m(4, tp=1)
            result["quality"] = m(16, tp=1)
            run["baselines"][baseline]["metrics"] = result
    return data


@pytest.fixture
def setup_ui(tmp_path, monkeypatch):
    data = ui_data()
    manifest = write_fixture(tmp_path, data)
    build = reporting_adapter.build_bundle
    monkeypatch.setattr(reporting_adapter, "build_bundle",
                        lambda root: build(tmp_path, manifest))
    return data, manifest, tmp_path


def app():
    result = AppTest.from_file(str(ROOT/"streamlit_app.py"), default_timeout=20).run()
    assert not result.exception
    result.sidebar.radio(key="page").set_value("Evidence & methods").run()
    assert not result.exception
    return result


def cards(at):
    return {item.label: item.value for item in at.metric}


def text(at):
    return "\n".join(str(item.value) for kind in
                     (at.caption, at.markdown, at.info, at.warning, at.error) for item in kind)


def evidence(at):
    return json.loads(at.json[0].value)


def counts(at, index=0):
    frame = at.table[index].value
    return dict(zip(frame["Measure"], frame["Count"], strict=True))


def test_survey_choices_values_units_provenance_and_navigation(setup_ui):
    at = app()
    assert "TEST FIXTURE" in text(at)
    assert cards(at)["Crop participation"] == "66.67%"
    assert cards(at)["Valid household responses"] == "3"
    assert "2 yes / 3 valid household responses" in text(at)
    assert counts(at)["Missing responses"] == "1"
    assert "not national or current prevalence" in text(at)
    assert not any("Area measurement" in item.value for item in at.warning)
    assert "April-October 2022" in text(at)
    assert "Bundle built (UTC)" in text(at)
    at.selectbox(key="indicator").select("NASS-02").run()
    assert not at.exception
    assert cards(at)["Lower bound (labelled m²)"] == "3.00"
    assert cards(at)["Upper bound (labelled m²)"] == "5.00"
    assert cards(at)["Bound width (labelled m²)"] == "2.00"
    assert counts(at)["Missing area values"] == "1"
    assert "separate reference): 4.00" in text(at)
    assert "not confidence intervals" in text(at)
    assert "Measurement lineage is unverified" in text(at)
    assert any("Area measurement" in item.value for item in at.warning)
    assert any(item.value == "Source: TEST FIXTURE" for item in at.caption)
    assert evidence(at)["values"]["width_m2"] == 2
    assert set(evidence(at)["provenance"]) == {"nass01.json", "nass02.json"}
    at.sidebar.radio(key="view").set_value("Synthetic quality").run()
    at.sidebar.radio(key="view").set_value("Survey findings").run()
    assert not at.exception
    assert "TEST FIXTURE" in text(at)
    assert len(at.selectbox) == 1  # no geographic/unsupported filter controls


@pytest.mark.parametrize("seed", (303, 404, 505))
@pytest.mark.parametrize("scenario", ("Clean", "Exact-repeat", "Mixed"))
@pytest.mark.parametrize("baseline", ("B0", "B1"))
def test_every_quality_cell_and_selection_transition(setup_ui, seed, scenario, baseline):
    data, _, _ = setup_ui
    run = next(r for r in data["m3_04_evaluation.json"]["runs"]
               if r["seed"] == seed and r["configuration"] == scenario)
    at = app()
    at.sidebar.radio(key="view").set_value("Synthetic quality").run()
    at.selectbox(key="seed").select(seed)
    at.selectbox(key="scenario").select(scenario)
    at.selectbox(key="baseline").select(baseline).run()
    for mode, measures in (("Matching", ("same_person", "duplicate_role")),
                           ("Field quality", ("quality", *reporting_adapter.RULES))):
        at.radio(key="evaluation").set_value(mode).run()
        key = "relation" if mode == "Matching" else "rule"
        for measure in measures:
            at.selectbox(key=key).select(measure).run()
            assert not at.exception
            expected = run["baselines"][baseline]["metrics"]
            metric = expected[measure] if measure in expected else expected["quality_by_rule"][measure]
            assert evidence(at)["selected_cell"] == {
                "seed": seed, "configuration": scenario, "baseline": baseline, "measure": measure}
            assert cards(at)["Submission events"] == str(run["events"])
            assert cards(at)["True synthetic people"] == str(run["people"])
            assert cards(at)["Intended roles"] == str(run["intended_roles"])
            for name, label in (("precision", "Precision"), ("recall", "Recall"),
                                ("false_positive_rate", "False-positive rate")):
                assert cards(at)[label] == percentage(metric[name])
            assert evidence(at)["counts"]["universe"] == metric["universe"]
            assert counts(at)["Actual positives (TP + FN)"] == str(metric["tp"]+metric["fn"])
            assert f"Precision: {metric['tp']+metric['fp']}" in text(at)
            assert f"Recall: {metric['tp']+metric['fn']}" in text(at)
            assert f"False-positive rate: {metric['fp']+metric['tn']}" in text(at)
            if metric["precision"] is None:
                assert "Precision is not defined: no predicted positives" in text(at)
            if metric["recall"] is None:
                assert "Recall is not defined: no actual positives" in text(at)
            assert "TEST FIXTURE" in text(at)
            assert "no automatic merging" in text(at).lower()
            assert not at.get("file_uploader") and not at.get("download_button")


@pytest.mark.parametrize("size,collision", [(1000, False), (10000, False), (55000, False),
                                           (100000, False), (300, True), (1000, True)])
def test_every_workload_measure_and_rejection(setup_ui, size, collision):
    at = app()
    at.sidebar.radio(key="view").set_value("Workload measurements").run()
    at.selectbox(key="workload").select(f"{size}:{int(collision)}").run()
    for mode, unit, median, repetitions in (("timing", "seconds", "3.000", 5),
                                           ("traced_allocation", "MiB", "11.00", 3)):
        at.radio(key="measurement").set_value(mode).run()
        assert not at.exception
        assert evidence(at)["selected_cell"] == {"events": size, "collision": collision}
        assert counts(at)["Submission events"] == integer(size)
        assert "TEST FIXTURE" in text(at)
        if size == 1000 and collision:
            assert not at.metric
            assert "Rejected: candidate budget exceeded" in text(at)
            assert "499,500 potential pairs / 250,000 allowed" in text(at)
            assert "not zero measurements" in text(at)
            assert len(at.table) == 1
            assert not at.get("vega_lite_chart")
        else:
            assert cards(at)[f"Median ({unit})"] == median
            assert len(at.table[1].value) == repetitions
            assert "Every measured repetition retained" in text(at)
            assert "Shared-machine" in text(at) if mode == "timing" else "Not process RSS" in text(at)
            assert evidence(at)["units"][mode] == unit
            charts = at.get("vega_lite_chart")
            assert len(charts) == 1 and unit in charts[0].proto.spec


def test_manual_default_and_method_relation_denominator_changes(setup_ui):
    at = app()
    at.sidebar.radio(key="view").set_value("Synthetic quality").run()
    assert at.selectbox(key="scenario").value == "Mixed"
    assert at.selectbox(key="baseline").value == "B1"
    assert at.selectbox(key="relation").value == "duplicate_role"
    assert cards(at)["Precision"] == "50.00%"
    assert cards(at)["Recall"] == "100.00%"
    assert cards(at)["False-positive rate"] == "20.00%"
    assert "Precision: 2" in text(at) and "Recall: 1" in text(at)
    at.selectbox(key="baseline").select("B0").run()
    assert cards(at)["Precision"] == "0.00%" and cards(at)["Recall"] == "0.00%"
    assert "Precision: 1" in text(at)
    at.selectbox(key="baseline").select("B1")
    at.selectbox(key="relation").select("same_person").run()
    assert cards(at)["Precision"] == "75.00%"
    assert "Precision: 4" in text(at) and "Recall: 3" in text(at)
    assert evidence(at)["counts"]["universe"] == 6


@pytest.mark.parametrize("state", ("undefined", "unbounded", "zero"))
def test_area_special_states_render_without_conflation(setup_ui, state):
    data, manifest, root = setup_ui
    e = data["nass02.json"]["estimates"]
    n = 0 if state == "undefined" else 1
    known = 1 if state == "zero" else 0
    e.update(total_plots=n, observed_areas=known, missing_areas=n-known,
             middle_lower_rank=1 if n else None, middle_upper_rank=1 if n else None,
             observed_only_median_m2=0 if known else None,
             full_roster_lower_m2=0 if n else None, full_roster_upper_m2=0 if known else None,
             width_m2=0 if known else None, status="bounded" if known else state)
    manifest.update(write_fixture(root, data))
    at = app()
    at.selectbox(key="indicator").select("NASS-02").run()
    assert not at.exception
    expected = "Unbounded" if state == "unbounded" else "0.00" if known else "Not defined"
    assert cards(at)["Upper bound (labelled m²)"] == expected
    assert evidence(at)["status"] == ("bounded" if known else state)


def test_zero_valid_responses_and_live_unavailability(setup_ui):
    data, manifest, root = setup_ui
    data["nass01.json"]["counts_and_rates"].update(
        input_rows=1, numerator=0, denominator=0, no_count=0, missing_count=1,
        invalid_count=0, excluded_count=1, proportion=None, percentage=None)
    manifest.update(write_fixture(root, data))
    at = app()
    assert cards(at)["Crop participation"] == "Not defined"
    assert "no valid responses" in text(at)
    (root/"reports/private/nass02.json").write_text('{}', encoding='utf-8')
    at.run()
    assert not at.exception and not at.metric
    assert "Evidence unavailable" in text(at)
    assert not at.selectbox
    at.sidebar.radio(key="view").set_value("Synthetic quality").run()
    assert not at.exception and at.metric
    assert "TEST FIXTURE" in text(at)


def test_manifest_failure_has_safe_message_without_path(monkeypatch):
    def broken(root):
        raise ValueError("DO-NOT-SHOW-PRIVATE-PATH")

    monkeypatch.setattr(reporting_adapter, "build_bundle", broken)
    at = app()
    assert "Evidence unavailable" in text(at)
    assert "DO-NOT-SHOW" not in text(at)
    assert not at.metric and not at.json


@pytest.mark.parametrize("value,expected", [(None, "Not defined"), (0, "0.00%"),
                                          (0.5, "50.00%"), (0.000001, "<0.01%")])
def test_percentage_rounding_has_independent_expected_values(value, expected):
    assert percentage(value) == expected


def test_precision_and_count_formatting_and_local_config():
    import tomllib

    assert integer(55000) == "55,000"
    assert decimal(6070.290058851242, 2) == "6,070.29"
    assert decimal(1.0706228999915766, 3) == "1.071"
    assert decimal(16.64679527282715, 2) == "16.65"
    assert decimal(None, 2) == "Not defined"
    assert decimal(None, 2, True) == "Unbounded"
    assert build_time("2026-10-29T18:10:00.123456+00:00") == "2026-10-29 18:10:00"
    config = tomllib.loads((ROOT/".streamlit/config.toml").read_text())
    assert config["server"] == {"address": "127.0.0.1", "headless": True}
    assert config["browser"]["gatherUsageStats"] is False
    assert config["client"]["showErrorDetails"] == "none"
    assert COUNT_LABELS["no_count"] == "Answered no (code 2)"
