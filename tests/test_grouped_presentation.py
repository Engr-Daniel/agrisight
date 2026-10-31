"""Single-level subject navigation, deep links and concise context preserve interpretation."""

from test_stakeholder_product import app, subject, text

from agrisight.stakeholder_site import SUBJECTS


def html(at):
    return "\n".join(i.value for i in at.get("html"))


def test_every_subject_is_one_tap_away_and_labelled_with_its_topic(monkeypatch):
    at = subject(app(monkeypatch))
    assert not at.exception
    chips = at.pills(key="subject")
    assert list(chips.options) == list(SUBJECTS)
    assert len(SUBJECTS) == 9 and not at.tabs  # no nested tab bars
    for name, (topic, _scene, _icon, question, _lead) in SUBJECTS.items():
        at.pills(key="subject").set_value(name).run()
        assert not at.exception, name
        assert f"Agricultural insights · {topic}".replace("&", "&amp;") in html(at)
        assert question in html(at)
        assert "these are not national estimates" in text(at)


def test_deselecting_a_chip_keeps_the_current_subject(monkeypatch):
    at = subject(app(monkeypatch), "Seed sources")
    at.pills(key="subject").set_value(None).run()
    assert not at.exception and at.pills(key="subject").value == "Seed sources"


def test_subject_survives_a_visit_to_another_page(monkeypatch):
    at = subject(app(monkeypatch), "Plot types")
    at.button(key="nav_2").click().run()
    at.button(key="nav_1").click().run()
    assert not at.exception and at.pills(key="subject").value == "Plot types"
    assert "What kinds of plots were recorded?" in [h.value for h in at.subheader]


def test_overview_topic_buttons_deep_link_into_insights(monkeypatch):
    at = app(monkeypatch)
    at.button(key="open_Water management").click().run()
    assert not at.exception and at.pills(key="subject").value == "Water management"
    assert "Water Management" in [h.value for h in at.subheader]
    assert "irrigation evidence is unavailable" in text(at)  # fixture has no irrigation artifact


def test_grouped_context_disclosures_and_data_quality(monkeypatch):
    at = subject(app(monkeypatch))
    assert "these are not national estimates" in text(at)
    assert "Households may report multiple activities" in text(at)
    assert any("Understanding these figures" in e.label for e in at.expander)
    assert "Illustrations are original AgriSight artwork" in html(at)
    assert "AI-generated" not in html(at) + text(at)
    at.button(key="nav_2").click().run()
    assert not at.exception
    assert "Crop portfolio coverage" in [h.value for h in at.subheader]
    assert "Input quantity completeness" in [h.value for h in at.subheader]
    assert "coverage details are hidden" in text(at)
    assert "completeness details are hidden" in text(at)


def test_overview_tells_the_story_from_bundle_values(monkeypatch):
    at = app(monkeypatch)
    page = html(at)
    assert not at.exception and not at.selectbox  # the explorer lives on Insights
    assert 'class="agri-hero2"' in page and page.count('class="agri-slide"') == 6
    assert page.count('class="agri-activity-card"') == 4
    assert "66.7%" in page  # fixture crops share 2/3, not a hard-coded survey value
    assert 'class="agri-mosaic"' in page and "Households surveyed" in page
    assert "Temporary crop types" not in page  # optional evidence unavailable in the fixture
    assert "national estimates" in text(at)
