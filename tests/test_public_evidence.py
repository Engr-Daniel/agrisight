"""Hosted mode shows only reviewed display aggregates and fails closed."""

import copy
import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest
from test_stakeholder_product import fixture_data

from agrisight import public_evidence as pe
from agrisight import stakeholder_reporting as adapter

ROOT = Path(__file__).resolve().parents[1]


def core():
    return {"status": "available", "origin": "REVIEWED LOCAL EVIDENCE", **adapter.project(fixture_data())}


def write_public(root, bundles):
    path = root/pe.PUBLIC_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"public_evidence_version": "1.0", "bundles": bundles}), encoding="utf-8")


def bundles():
    return {"core": core(), **{name: {"status": "unavailable"} for name in pe.NAMES if name != "core"}}


def test_forbidden_keys_found_at_any_depth():
    assert pe.forbidden_keys({"a": [{"HHID": 1}], "b": {"gps": 2}}) == ["/a/0/HHID", "/b/gps"]
    assert pe.forbidden_keys({"name": "Kano", "households": 9}) == []


def test_hosted_evidence_reads_only_the_public_file(tmp_path, monkeypatch):
    write_public(tmp_path, bundles())
    monkeypatch.setattr(adapter, "build_bundle", lambda root: pytest.fail("private adapter used"))
    ev = pe.Evidence(tmp_path, hosted=True)
    assert ev.hosted and ev.get("core")["status"] == "available"
    assert ev.get("seed") == {"status": "unavailable"}


@pytest.mark.parametrize("mutate", [
    lambda d: d.pop("crop"),
    lambda d: d["core"].update(status="unavailable"),
    lambda d: d["core"]["activities"][0].update(hhid=1),
])
def test_malformed_public_file_fails_closed(tmp_path, mutate):
    data = bundles()
    mutate(data)
    write_public(tmp_path, data)
    assert pe.load(tmp_path) is None
    assert pe.Evidence(tmp_path, hosted=True).get("core") == {"status": "unavailable"}


def test_missing_public_file_fails_closed(tmp_path):
    assert pe.load(tmp_path) is None


def test_build_refuses_fixture_or_unavailable_evidence(tmp_path, monkeypatch):
    monkeypatch.setattr(adapter, "build_bundle", lambda root: {**core(), "origin": "TEST FIXTURE"})
    with pytest.raises(ValueError):
        pe.build(tmp_path)
    monkeypatch.setattr(adapter, "build_bundle", lambda root: {"status": "unavailable"})
    with pytest.raises(ValueError):
        pe.build(tmp_path)


def test_committed_public_file_is_valid_and_cited():
    data = json.loads((ROOT/pe.PUBLIC_PATH).read_text(encoding="utf-8"))
    assert pe.load(ROOT) is not None and data["citation"] == pe.CITATION
    assert all(b["status"] == "available" and b.get("origin") != "TEST FIXTURE"
               for b in data["bundles"].values())
    assert b"\r" not in (ROOT/pe.PUBLIC_PATH).read_bytes()


def test_public_app_renders_every_page_from_the_public_file():
    at = AppTest.from_file(str(ROOT/"public_app.py"), default_timeout=60).run()
    assert not at.exception and "NGA-NBS-NASS-2023-V01" in "".join(h.value for h in at.get("html"))
    for i in range(5):
        at.button(key=f"nav_{i}").click().run()
        assert not at.exception, i
    at.button(key="nav_1").click().run()
    for name in ("Crop portfolio", "Seed sources", "Water management", "Sales & storage"):
        at.pills(key="subject").set_value(name).run()
        assert not at.exception and not any("unavailable" in i.value for i in at.info), name
    at.button(key="nav_4").click().run()
    assert pe.CITATION in [m.value for m in at.markdown]


def test_live_mode_is_unchanged_without_public_flag(monkeypatch):
    calls = []
    monkeypatch.setattr(adapter, "build_bundle", lambda root: calls.append(root) or copy.deepcopy(core()))
    assert pe.Evidence(ROOT).get("core")["status"] == "available" and calls
