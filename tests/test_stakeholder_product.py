"""Product accounting, fail-closed loading and all five stakeholder pages."""

import copy
import hashlib
import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest
from test_stakeholder_analysis import frames

from agrisight import stakeholder_analysis as model
from agrisight import stakeholder_reporting as adapter

ROOT = Path(__file__).resolve().parents[1]


def fixture_data():
    return {"analysis_version": "1.0", **model.calculate(*frames())}


def write_fixture(root, data):
    path = root / "reports/private/stakeholder_sa1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(data).encode()
    path.write_bytes(raw)
    return {"purpose": "TEST FIXTURE", "artifact": {
        "sha256": hashlib.sha256(raw).hexdigest(), "expected": {"analysis_version": "1.0"}}}


def test_projection_and_private_fields_removed():
    data = fixture_data()
    data["raw_identity"] = "never forward"
    result = adapter.project(data)
    assert result["activities"][0]["share"] == 2/3
    assert "raw_identity" not in result
    assert result["overlap"]["excluded"] == 2


@pytest.mark.parametrize("mutation", [
    lambda d: d["activities"][0].update(yes=True),
    lambda d: d["activities"][0].update(denominator=99),
    lambda d: d["activities"][0].update(share=0.9),
    lambda d: d["activities"].reverse(),
    lambda d: d["overlap"].update(excluded=0),
    lambda d: d["overlap"]["cells"][0].update(count=99),
    lambda d: d["overlap"]["cells"][0].update(crops="no"),
    lambda d: d["plot_types"][0].update(count=99),
    lambda d: d["plots"].update(recorded_area=0),
])
def test_invalid_aggregate_rejected(mutation):
    data = fixture_data()
    mutation(data)
    with pytest.raises(ValueError):
        adapter.project(data)


def test_loading_is_hash_pinned_and_fails_closed(tmp_path):
    manifest = write_fixture(tmp_path, fixture_data())
    assert adapter.build_bundle(tmp_path, manifest)["status"] == "available"
    path = tmp_path / "reports/private/stakeholder_sa1.json"
    path.write_bytes(path.read_bytes() + b" ")
    assert adapter.build_bundle(tmp_path, manifest) == {"status": "unavailable"}
    path.unlink()
    assert adapter.build_bundle(tmp_path, manifest) == {"status": "unavailable"}


def app(monkeypatch, data=None):
    bundle = {"status": "available", "origin": "TEST FIXTURE",
              **adapter.project(data or fixture_data())}
    monkeypatch.setattr(adapter, "build_bundle", lambda root: copy.deepcopy(bundle))
    return AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=25).run()


def text(at):
    return "\n".join(item.value for kind in ("markdown", "caption", "warning", "info")
                     for item in at.get(kind))


def test_five_pages_activity_selection_and_source_context(monkeypatch):
    at = app(monkeypatch)
    assert not at.exception and not at.json
    assert at.selectbox(key="activity").value == "all"
    for i in ("crops", "livestock", "fish_capture", "fish_farming", "all"):
        at.selectbox(key="activity").set_value(i).run()
        assert not at.exception
    for i in range(5):
        at.button(key=f"nav_{i}").click().run()
        assert not at.exception and not at.json
        assert "NASS" in text(at)
        assert "national estimates" in text(at) or "National inference" in text(at)
    assert not any(b.label in ("Engineering studies", "Evidence & methods") for b in at.button)
    assert "learning" not in text(at).lower()


def test_undefined_share_and_unavailable_about(monkeypatch):
    hh, pp = frames()
    hh["s00_q15a"] = None
    data = {"analysis_version": "1.0", **model.calculate(hh, pp)}
    at = app(monkeypatch, data)
    at.selectbox(key="activity").set_value("crops").run()
    assert not at.exception
    assert "Undefined" in [m.value for m in at.metric]
    monkeypatch.setattr(adapter, "build_bundle", lambda root: {"status": "unavailable"})
    at.run()
    assert not at.metric and "Findings are hidden" in text(at)
    for i in (1, 2, 3):
        at.button(key=f"nav_{i}").click().run()
        assert not at.exception and not at.metric
    at.button(key="nav_4").click().run()
    assert not at.exception and "Source and scope" in [s.value for s in at.subheader]
