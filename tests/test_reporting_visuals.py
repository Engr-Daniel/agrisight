"""Stakeholder illustrations draw only the values they are given, honestly rounded."""

import base64
import re

import pytest

from agrisight import reporting_visuals as visuals


@pytest.mark.parametrize("proportion,squares", [
    (0.0, 0), (1.0, 100), (0.9284022221445791, 93), (0.5, 50),
    (0.004, 0), (0.996, 100), (0.0001, 0), (0.9999, 100)])
def test_per_hundred_preserves_the_rounded_scale(proportion, squares):
    assert visuals.per_hundred(proportion) == squares


@pytest.mark.parametrize("bad", [-0.01, 1.01])
def test_per_hundred_rejects_impossible_shares(bad):
    with pytest.raises(ValueError):
        visuals.per_hundred(bad)


def drawing(html):
    return base64.b64decode(re.search(r"base64,([A-Za-z0-9+/=]+)", html).group(1)).decode()


def test_waffle_fills_exactly_the_rounded_share_and_labels_it():
    out = visuals.waffle(2/3, "grew crops", "did not")
    svg = drawing(out)
    assert svg.count(f'fill="{visuals.LEAF}"') == 67
    assert svg.count(f'fill="{visuals.PALE}"') == 33
    assert 'alt="About 67 in every 100 grew crops; 33 in every 100 did not."' in out
    assert "rounded" in out and "<svg" not in out  # sanitiser-safe image, not inline SVG


def test_waffle_undefined_share_is_stated_not_drawn_as_zero():
    out = visuals.waffle(None, "grew crops", "did not")
    assert "agri-waffle" not in out and "Not defined" in out


def test_waffle_escapes_labels():
    out = visuals.waffle(0.5, "<b>yes</b>", 'no"')
    assert "<b>" not in out and "&lt;b&gt;yes" in out and "no&quot;" in out


def test_plot_square_is_to_scale_and_converts_units():
    svg = drawing(visuals.plot_square(10_000))
    assert "1.00 ha" in svg and "100 m × 100 m" in svg
    assert 'width="150.0"' in svg  # one hectare fills the 100 m reference
    small = drawing(visuals.plot_square(2_500))
    assert "0.25 ha" in small and 'width="75.0"' in small
    assert "about 0.25 hectares" in visuals.plot_square(2_500)


def test_plot_square_expands_its_reference_for_large_areas():
    svg = drawing(visuals.plot_square(40_000))
    assert 'width="150.0"' in svg and "200 m" in svg and "to scale vs 4 ha" in svg
    assert "200 m by 200 m reference" in visuals.plot_square(40_000)
    assert "not an observed plot shape" in visuals.plot_square(40_000)


@pytest.mark.parametrize("area", [None, -1, float("nan"), float("inf")])
def test_plot_square_draws_nothing_for_missing_or_invalid_area(area):
    assert visuals.plot_square(area) == ""


@pytest.mark.parametrize("share", [0.0001, 0.9999])
def test_sub_square_groups_are_labelled_nonzero_without_exaggeration(share):
    out = visuals.waffle(share, "yes", "no")
    assert "smaller group is nonzero" in out and "Exact share:" in out
    assert drawing(out).count(f'fill="{visuals.LEAF}"') == round(share*100)


def test_map_slot_has_no_geography_or_values():
    out = visuals.map_pending()
    caption = re.sub(r"<[^>]+>", " ", out.split("<figcaption>")[1])
    assert not re.search(r"\d", caption)
    assert "no regional values" in caption
    art = drawing(out)
    assert art.count("<path") == 1 and "<text" not in art  # one decorative line, no labels


def test_text_builders_escape_content():
    assert "<script>" not in visuals.section("<script>", "x", "y")
    assert "<script>" not in visuals.banner("a", "<script>", "c", "sprout")
    assert "<script>" not in visuals.steps([("check", "<script>", "b")])
