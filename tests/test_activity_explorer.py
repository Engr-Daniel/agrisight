"""Activity comparison semantics and selector transitions with manually counted fixtures."""

from test_stakeholder_product import app, text

from agrisight.activity_explorer import chart


def html(at):
    return "\n".join(i.value for i in at.get("html"))


def test_default_all_four_bars_and_both_units(monkeypatch):
    at = app(monkeypatch)
    assert at.selectbox(key="activity").value == "all"
    assert at.radio(key="activity_unit").value == "Percentages"
    assert html(at).count('class="agri-activity-row"') == 4
    assert "66.67%" in html(at) and "100% of valid responses" in html(at)
    assert "denominators differ" in text(at) and "Responses can overlap" in text(at)
    assert "same-season" in text(at)
    at.radio(key="activity_unit").set_value("Household counts").run()
    assert not at.exception
    assert "5 household records" in html(at)
    assert "<strong>2</strong>" in html(at)
    assert "<strong>66.67%</strong>" not in html(at)


def test_focus_breakdown_interpretation_and_return_to_all(monkeypatch):
    at = app(monkeypatch)
    for identifier, percentage, yes in (("crops", "66.67%", "2"),
                                      ("livestock", "60.00%", "3"),
                                      ("fish_capture", "20.00%", "1"),
                                      ("fish_farming", "20.00%", "1")):
        at.selectbox(key="activity").set_value(identifier).run()
        assert not at.exception
        assert html(at).count('class="agri-activity-row"') == 1
        assert {m.label: m.value for m in at.metric}["Share of valid responses"] == percentage
        assert {m.label: m.value for m in at.metric}["Households reporting activity"] == yes
        breakdown = at.dataframe[0].value
        assert list(breakdown["Response"]) == ["Yes", "No", "Missing", "Invalid"]
        assert sum(breakdown["Households"]) == 5
        assert "production, income or service need" in text(at)
        at.radio(key="activity_unit").set_value("Household counts").run()
        assert not at.exception and f"<strong>{yes}</strong>" in html(at)
        at.radio(key="activity_unit").set_value("Percentages").run()
    at.selectbox(key="activity").set_value("all").run()
    assert not at.metric and html(at).count('class="agri-activity-row"') == 4
    at.button(key="nav_1").click().run()
    assert not at.exception and at.selectbox(key="activity").value == "all"


def test_zero_and_undefined_are_distinct_and_labels_escaped():
    item = {"id": "crops", "label": "<script>bad</script>", "yes": 0,
            "share": None, "input_rows": 5, "denominator": 0, "period": "test"}
    output = chart([item], "Percentages")
    assert "Undefined" in output and "<script>" not in output
    assert "&lt;script&gt;" in output
    item["share"] = 0
    item["denominator"] = 5
    assert "<strong>0.00%</strong>" in chart([item], "Percentages")
    assert "<strong>0</strong>" in chart([item], "Household counts")
