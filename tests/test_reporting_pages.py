"""Both presentation layers use verified fixtures and correct evidence destinations."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest
from test_reporting_adapter import write_fixture
from test_reporting_ui import cards, evidence, text, ui_data

from agrisight import reporting_adapter

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    data = ui_data()
    manifest = write_fixture(tmp_path, data)
    build = reporting_adapter.build_bundle
    monkeypatch.setattr(reporting_adapter, "build_bundle",
                        lambda root: build(tmp_path, manifest))
    return data, manifest, tmp_path


def html(at):
    return "\n".join(item.value for item in at.get("html"))


def home():
    at = AppTest.from_file(str(ROOT/"research_explorer_app.py"), default_timeout=20).run()
    assert not at.exception
    return at


def test_default_is_stakeholder_layer_not_technical_console(fixture):
    at = home()
    assert at.sidebar.radio(key="page").value == "Overview"
    assert cards(at) == {"Household records": "4", "Plot records": "3",
                         "Crop participation": "66.67%"}
    assert not at.selectbox and not at.json
    assert "TEST FIXTURE" in text(at) and "not added" in text(at)
    assert "not national" in text(at).lower()
    assert not any(k in cards(at) for k in ("Precision", "Submission events"))


def test_insights_ctas_reach_the_corresponding_indicator(fixture):
    at = home()
    at.button(key="explore_insights").click().run()
    assert not at.exception and not at.json
    assert cards(at)["Crop participation"] == "66.67%"
    assert cards(at)["Missing area values"] == "1"
    assert cards(at)["Lower median bound (labelled m²)"] == "3.00"
    assert html(at).count('class="agri-waffle"') == 1
    assert "About 67 in every 100 grew main-season crops" in html(at)
    at.button(key="participation_evidence").click().run()
    assert at.sidebar.radio(key="page").value == "Evidence & methods"
    assert at.selectbox(key="indicator").value == "NASS-01"
    assert evidence(at)["counts"]["denominator"] == 3
    at.sidebar.radio(key="page").set_value("Agricultural insights").run()
    at.button(key="area_evidence").click().run()
    assert at.selectbox(key="indicator").value == "NASS-02"
    assert evidence(at)["counts"]["missing_areas"] == 1


def test_engineering_link_resets_stale_controls_to_summary_cell(fixture):
    at = home()
    at.sidebar.radio(key="page").set_value("Engineering studies").run()
    assert "TEST FIXTURE" in text(at) and "Synthetic" in text(at)
    assert cards(at)["Precision"] == "50.00%"
    at.button(key="matching_evidence").click().run()
    at.selectbox(key="seed").select(505)
    at.selectbox(key="baseline").select("B0")
    at.radio(key="evaluation").set_value("Field quality").run()
    at.sidebar.radio(key="page").set_value("Engineering studies").run()
    at.button(key="matching_evidence").click().run()
    assert at.selectbox(key="seed").value == 303
    assert at.selectbox(key="baseline").value == "B1"
    assert at.radio(key="evaluation").value == "Matching"
    assert evidence(at)["selected_cell"]["measure"] == "duplicate_role"
    at.sidebar.radio(key="page").set_value("Engineering studies").run()
    at.button(key="workload_evidence").click().run()
    assert at.selectbox(key="workload").value == "55000:0"
    assert at.radio(key="measurement").value == "timing"


def test_missing_survey_never_leaves_stale_home_numbers(fixture):
    _, _, root = fixture
    at = home()
    assert at.metric
    (root/"reports/private/nass02.json").write_text('{}', encoding="utf-8")
    at.run()
    assert not at.metric and "Survey findings are unavailable" in text(at)
    at.sidebar.radio(key="page").set_value("Agricultural insights").run()
    assert not at.metric and 'class="agri-waffle"' not in html(at)
    at.sidebar.radio(key="page").set_value("Engineering studies").run()
    assert cards(at)["Precision"] == "50.00%" and not at.exception


def test_undefined_participation_is_not_zero_or_a_positive_claim(fixture):
    data, manifest, root = fixture
    data["nass01.json"]["counts_and_rates"].update(
        input_rows=1, numerator=0, denominator=0, no_count=0, missing_count=1,
        invalid_count=0, excluded_count=1, proportion=None, percentage=None)
    manifest.update(write_fixture(root, data))
    at = home()
    assert cards(at)["Crop participation"] == "Not defined"
    at.sidebar.radio(key="page").set_value("Agricultural insights").run()
    assert cards(at)["Crop participation"] == "Not defined"
    assert "no valid responses" in text(at)
    assert 'class="agri-waffle"' not in html(at) and "Not defined: no valid responses" in html(at)


def test_about_does_not_require_analytical_inputs(monkeypatch):
    def broken(root):
        raise ValueError("PRIVATE-DETAIL")

    monkeypatch.setattr(reporting_adapter, "build_bundle", broken)
    at = home()
    at.sidebar.radio(key="page").set_value("About").run()
    assert not at.exception and not at.error
    assert "portfolio prototype" in text(at) and "PRIVATE-DETAIL" not in text(at)


@pytest.mark.parametrize("state", ["undefined", "unbounded", "zero"])
def test_stakeholder_area_states_keep_their_meaning(fixture, state):
    data, manifest, root = fixture
    n = 0 if state == "undefined" else 1
    known = int(state == "zero")
    data["nass02.json"]["estimates"].update(
        total_plots=n, observed_areas=known, missing_areas=n-known,
        middle_lower_rank=1 if n else None, middle_upper_rank=1 if n else None,
        observed_only_median_m2=0 if known else None,
        full_roster_lower_m2=0 if n else None, full_roster_upper_m2=0 if known else None,
        width_m2=0 if known else None, status="bounded" if known else state)
    manifest.update(write_fixture(root, data))
    at = home()
    at.sidebar.radio(key="page").set_value("Agricultural insights").run()
    assert not at.exception
    if state == "zero":
        assert cards(at)["Upper median bound (labelled m²)"] == "0.00"
    else:
        assert "Upper median bound (labelled m²)" not in cards(at)
        assert ("not defined" if state == "undefined" else "no finite upper") in text(at)


@pytest.mark.parametrize("name,hidden", [("m3_04_evaluation.json", "Precision"),
                                        ("m3_05_benchmark.json", "Submission events")])
def test_engineering_panels_fail_independently(fixture, name, hidden):
    _, _, root = fixture
    (root/"reports/private"/name).write_text('{}', encoding="utf-8")
    at = home()
    assert cards(at)["Crop participation"] == "66.67%"
    at.sidebar.radio(key="page").set_value("Engineering studies").run()
    assert not at.exception and hidden not in cards(at)
    assert "Study evidence is unavailable" in text(at)
    assert "Submission events" in cards(at) if hidden == "Precision" else "Precision" in cards(at)


def test_top_navigation_and_back_link_change_pages_only(fixture):
    at = home()
    assert at.button(key="nav_0").proto.type == "primary"  # Overview is current
    at.button(key="nav_1").click().run()
    assert at.sidebar.radio(key="page").value == "Agricultural insights"
    at.button(key="participation_evidence").click().run()
    assert at.radio(key="view").value == "Survey findings"
    at.button(key="back_to_site").click().run()
    assert not at.exception
    assert at.sidebar.radio(key="page").value == "Agricultural insights"
    assert cards(at)["Crop participation"] == "66.67%"


def test_overview_story_and_map_slot_stay_within_evidence(fixture):
    at = home()
    body = html(at)
    assert "About 67 in every 100 grew main-season crops" in body
    assert 'class="agri-map"' in body and "no regional values" in body
    assert "AI-generated" not in body.split('class="agri-footer"')[0]
    assert "AI-generated illustration" in body  # credit kept in the footer
