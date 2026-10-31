"""Website builders draw only the values they are given; artwork carries no data."""

import base64
import html
import re
import xml.etree.ElementTree as ET
from importlib.resources import files

import pytest

from agrisight import site_art, website


def drawing(html):
    return base64.b64decode(re.search(r"base64,([A-Za-z0-9+/=]+)", html).group(1)).decode()


def overlap(yy, yn, ny, nn):
    cells = [{"crops": c, "livestock": l, "count": n}
             for (c, l), n in zip((("yes", "yes"), ("yes", "no"), ("no", "yes"), ("no", "no")),
                                  (yy, yn, ny, nn), strict=True)]
    return {"cells": cells, "denominator": yy + yn + ny + nn, "excluded": 0}


@pytest.mark.parametrize("name", list(site_art.SCENES))
def test_every_scene_is_valid_svg_with_alt_text_and_no_numbers(name):
    svg = site_art.drawing(name)
    ET.fromstring(svg)  # well-formed
    assert not re.search(r"<text[^>]*>[^<]*\d", svg)  # artwork never encodes a value
    out = site_art.scene(name)
    assert "<svg" not in out and 'alt="' in out and html.escape(site_art.SCENES[name][1]) in out
    assert 'alt=""' in site_art.scene(name, decorative=True)


def test_mosaic_areas_are_true_to_the_counts():
    out = website.overlap_mosaic(overlap(60, 20, 15, 5))
    svg = drawing(out)
    widths = [float(w) for w in re.findall(r'width="([\d.]+)"', svg)]
    heights = [float(h) for h in re.findall(r'height="([\d.]+)"', svg)]
    areas = [(w + 3) * (h + 3) for w, h in zip(widths, heights, strict=True)]  # add back the gap
    total = sum(areas)
    assert [round(a / total, 3) for a in areas] == [0.6, 0.2, 0.15, 0.05]
    assert "60.0%" in out and "60 households" in out and "Neither" in out
    assert "Mosaic of 100 households" in out


def test_mosaic_handles_empty_column_and_undefined_total():
    out = website.overlap_mosaic(overlap(3, 2, 0, 0))
    assert drawing(out).count("<rect") == 2 and "0.0%" in out
    assert "undefined" in website.overlap_mosaic(overlap(0, 0, 0, 0))


def test_activity_cards_show_counts_and_never_draw_undefined_as_zero():
    base = {"id": "crops", "label": "Main-season crops", "yes": 2, "denominator": 3,
            "period": "April–October 2022", "share": 2 / 3}
    out = website.activity_cards([base, {**base, "id": "livestock", "label": "<b>x</b>",
                                         "yes": 0, "denominator": 0, "share": None}])
    assert "66.7%" in out and "2 of 3 households" in out and "width:66.6667%" in out
    assert "Undefined" in out and "share undefined" in out and out.count("agri-card-bar") == 1
    assert "<b>x</b>" not in out and "&lt;b&gt;x" in out


def test_hero_slides_respect_reduced_motion_and_omit_unknown_counts():
    css = files("agrisight").joinpath("assets/website.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion: reduce" in css
    assert "what surveyed households reported" in website.hero(None)
    assert "143,105 surveyed households" in website.hero(143105)
    assert website.hero(1).count("agri-slide-art") == len(website.SLIDES)


def test_text_builders_escape_content():
    for out in (website.banner("<i>", "<script>", "x", "crops"), website.heading("<i>", "<script>"),
                website.figures([("<script>", "a", "b")]), website.steps([("<script>", "b")]),
                website.topic_card("crops", "<script>", "b"), website.footer("<script>")):
        assert "<script>" not in out
