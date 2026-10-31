"""Topic navigation and concise context preserve interpretation and failure states."""

from test_stakeholder_product import app, text


def test_grouped_topics_and_context_disclosures(monkeypatch):
    at = app(monkeypatch)
    at.button(key="nav_1").click().run()
    assert not at.exception
    labels = [t.label for t in at.tabs]
    positions = [labels.index(name) for name in ("Activities", "Crops & seeds", "Water & land", "Harvest & markets")]
    assert positions == sorted(positions) and positions[0] == 0
    assert all(label in labels for label in ("Crop portfolio", "Seed sources", "Input records",
        "Water management", "Land & travel", "Plot types", "Harvest difficulties", "Sales & storage"))
    assert "these are not national estimates" in text(at)
    assert "Households may report multiple activities" in text(at)
    assert any("Understanding these figures" in e.label for e in at.expander)
    assert "not a photograph of surveyed farms" not in text(at)
    assert "Illustration: AI-generated agricultural artwork" in text(at)
    at.button(key="nav_2").click().run()
    assert not at.exception
    assert "Crop portfolio coverage" in [h.value for h in at.subheader]
    assert "Input quantity completeness" in [h.value for h in at.subheader]
    assert "coverage details are hidden" in text(at)
    assert "completeness details are hidden" in text(at)
