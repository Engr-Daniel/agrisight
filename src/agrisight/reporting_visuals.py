"""Pure HTML/SVG builders for the stakeholder website layer.

Every number drawn here is passed in from the validated bundle; nothing is
hard-coded. Illustrations are explanatory pictures of those numbers and carry
a text equivalent. Streamlit's HTML sanitiser strips inline <svg>, so each
drawing is delivered as an <img> with an SVG data URI.
"""

import base64
from html import escape
from math import ceil, isfinite, sqrt

INK, LEAF, PALE, WHEAT = "#174d36", "#3f7d4a", "#dde4d2", "#e3c77d"
SERIF = "Georgia, 'Times New Roman', serif"

_ICONS = {
    "household": '<path d="M6 22 24 8l18 14"/><path d="M11 19v20h26V19"/>'
                 '<path d="M20 39V28h8v11"/>',
    "plots": '<path d="M5 34 18 14h12l13 20z"/><path d="M11 34l9-20M24 14v20M37 34l-9-20"/>'
             '<path d="M8 28h32M12 21h24"/>',
    "sprout": '<path d="M24 41V22"/><path d="M24 26c0-8-6-12-14-12 0 8 6 12 14 12z"/>'
              '<path d="M24 22c0-7 5-11 13-11 0 7-5 11-13 11z"/><path d="M14 41h20"/>',
    "survey": '<rect x="11" y="7" width="26" height="34" rx="3"/><path d="M18 7v5h12V7"/>'
              '<path d="m17 22 3 3 6-6M17 32h14"/>',
    "check": '<circle cx="24" cy="24" r="16"/><path d="m16 24 6 6 11-12"/>',
    "scale": '<path d="M24 8v32M12 40h24M10 14h28"/><path d="m10 14-5 12h10zM38 14l-5 12h10z"/>',
    "people": '<circle cx="17" cy="17" r="6"/><circle cx="33" cy="19" r="5"/>'
              '<path d="M6 39c1-8 5-12 11-12s10 4 11 12M28 39c1-6 3-9 8-9 4 0 6 3 7 9"/>',
    "shield": '<path d="M24 6 39 12v11c0 9-6 16-15 19-9-3-15-10-15-19V12z"/>'
              '<path d="m17 24 5 5 9-10"/>',
    "timer": '<circle cx="24" cy="27" r="14"/><path d="M24 27v-7M20 7h8M24 7v6M36 15l3-3"/>',
    "search": '<circle cx="21" cy="21" r="12"/><path d="m30 30 11 11"/>',
}


def svg(view_box: str, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">{body}</svg>'


def _image(drawing: str, alt: str = "", css: str = "", size: int | None = None) -> str:
    data = base64.b64encode(drawing.encode("utf-8")).decode("ascii")
    dimensions = f' width="{size}" height="{size}"' if size else ""
    return (f'<img class="{css}" src="data:image/svg+xml;base64,{data}" '
            f'alt="{escape(alt)}"{dimensions} />')


def icon(name: str, size: int = 44, colour: str = INK) -> str:
    """Decorative line icon (empty alt text)."""
    body = (f'<g fill="none" stroke="{colour}" stroke-width="2.2" stroke-linecap="round" '
            f'stroke-linejoin="round">{_ICONS[name]}</g>')
    return _image(svg("0 0 48 48", body), css="agri-icon", size=size)


def per_hundred(proportion: float) -> int:
    """Nearest whole squares out of 100; precise labels preserve small minorities."""
    if not 0 <= proportion <= 1:
        raise ValueError("proportion must be between 0 and 1")
    return round(proportion*100)


def waffle_drawing(filled: int) -> str:
    cells = []
    for index in range(100):
        row, column = divmod(index, 10)
        paint = f'fill="{LEAF}"' if index < filled else f'fill="{PALE}" stroke="#b8c4a8"'
        cells.append(f'<rect x="{column*22+1}" y="{row*22+1}" width="20" height="20" rx="4" '
                     f'{paint}/>')
    return svg("0 0 220 220", "".join(cells))


def waffle(proportion: float | None, yes_label: str, no_label: str) -> str:
    """A 10x10 unit picture of a part-to-whole share; says so when undefined."""
    if proportion is None:
        return (f'<div class="agri-art-icon agri-undefined">{icon("sprout", 96)}'
                '<p>Not defined: no valid responses to picture.</p></div>')
    filled = per_hundred(proportion)
    summary = f"About {filled} in every 100 {yes_label}; {100-filled} in every 100 {no_label}."
    note = "Each square is one in a hundred, rounded."
    if 0 < proportion < 1 and filled in (0, 100):
        note += (f" Exact share: {proportion*100:.6g}%. "
                 "The smaller group is nonzero but at most half a square.")
        summary = f"Rounded picture: {filled} of 100; exact share {proportion*100:.6g}%."
    return (f'<figure class="agri-waffle">{_image(waffle_drawing(filled), summary)}'
            f'<figcaption><span class="agri-key agri-key-yes"></span>{filled} {escape(yes_label)}'
            f'<span class="agri-key agri-key-no"></span>{100-filled} {escape(no_label)}'
            f'<small>{note}</small></figcaption></figure>')


def plot_drawing(area_m2: float) -> str:
    if not isfinite(area_m2) or area_m2 < 0:
        raise ValueError("area must be finite and nonnegative")
    side = sqrt(area_m2)
    reference = max(100, ceil(side/100)*100)
    box = 150 * side/reference
    return svg("0 0 330 190", (
        '<rect x="20" y="20" width="150" height="150" fill="none" stroke="#9fb18b" '
        'stroke-dasharray="5 5" rx="3"/>'
        f'<text x="95" y="14" text-anchor="middle" font-family="sans-serif" font-size="13" '
        f'fill="#526650">{reference:g} m</text>'
        f'<rect x="20" y="{170-box:.1f}" width="{box:.1f}" height="{box:.1f}" rx="3" '
        f'fill="#cfdcbc" stroke="{LEAF}" stroke-width="2"/>'
        f'<path d="M20 {170-box*.66:.1f}h{box:.1f}M20 {170-box*.33:.1f}h{box:.1f}" '
        f'stroke="{LEAF}" stroke-opacity=".35"/>'
        f'<text x="195" y="88" font-family="{SERIF}" font-size="26" fill="{INK}">'
        f'{area_m2/10_000:,.2f} ha</text>'
        f'<text x="195" y="112" font-family="sans-serif" font-size="13" fill="#526650">'
        f'{side:,.0f} m × {side:,.0f} m</text>'
        '<text x="195" y="132" font-family="sans-serif" font-size="13" fill="#526650">'
        f'to scale vs {reference**2/10_000:g} ha</text>'))


def plot_square(area_m2: float | None) -> str:
    """Equivalent square, with an adaptive labelled reference and no clipping."""
    if area_m2 is None or not isfinite(area_m2) or area_m2 < 0:
        return ""
    side = sqrt(area_m2)
    reference = max(100, ceil(side/100)*100)
    alt = (f"A square of {side:,.0f} m by {side:,.0f} m, about {area_m2/10_000:,.2f} hectares, "
           f"drawn to scale inside a {reference:g} m by {reference:g} m reference square.")
    return (f'<figure class="agri-plot">{_image(plot_drawing(area_m2), alt)}'
            '<figcaption>Equivalent square for illustration; not an observed plot shape. '
            'Uses released labelled units.</figcaption></figure>')


def section(eyebrow: str, title: str, lead: str = "") -> str:
    lead_html = f"<p>{escape(lead)}</p>" if lead else ""
    return (f'<div class="agri-heading"><span>{escape(eyebrow)}</span>'
            f'<h2>{escape(title)}</h2>{lead_html}</div>')


def banner(eyebrow: str, title: str, lead: str, art: str) -> str:
    """Inner-page banner: brand gradient, field-row pattern and a large icon."""
    return (f'<section class="agri-banner"><div><span>{escape(eyebrow)}</span>'
            f'<h1>{escape(title)}</h1><p>{escape(lead)}</p></div>'
            f'<div class="agri-banner-art">{icon(art, 96, WHEAT)}</div></section>')


def steps(items: list[tuple[str, str, str]]) -> str:
    """Numbered story steps: (icon, title, body)."""
    cards = "".join(
        f'<li><div class="agri-step-top">{icon(name, 40, WHEAT)}<b>{number:02d}</b></div>'
        f'<h3>{escape(title)}</h3><p>{escape(body)}</p></li>'
        for number, (name, title, body) in enumerate(items, 1))
    return f'<ol class="agri-steps">{cards}</ol>'


def stat_head(name: str, caption: str) -> str:
    return f'<div class="agri-stat-head">{icon(name)}<span>{escape(caption)}</span></div>'


def map_drawing() -> str:
    rings = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx+step*22}" ry="{ry+step*15}" '
        f'transform="rotate({angle} {cx} {cy})"/>'
        for cx, cy, rx, ry, angle in ((150, 120, 18, 12, -12), (370, 210, 14, 10, 18))
        for step in range(6))
    return svg("0 0 520 320", (
        '<rect width="520" height="320" fill="#e9efe0"/>'
        f'<g fill="none" stroke="#b9c9a6" stroke-width="1.4">{rings}</g>'
        '<path d="M0 270 C120 240 210 300 330 262 S470 230 520 250" fill="none" '
        'stroke="#cfdcbc" stroke-width="10" stroke-linecap="round"/>'))


def map_pending() -> str:
    """Map slot of the design system with no geography drawn.

    The contour artwork is abstract on purpose: no boundary source, sample support or
    disclosure review is approved yet, so no country/state shapes or values appear.
    """
    alt = "Abstract contour artwork. No geographic boundaries or regional values are shown."
    return (f'<figure class="agri-map">{_image(map_drawing(), alt)}'
            '<figcaption><b>Geographic view</b>'
            '<p>The source is a national agricultural sample survey. A state-level map is '
            'held back until a boundary source, sample support and disclosure checks are '
            'reviewed, so no regional values are shown here.</p></figcaption></figure>')
