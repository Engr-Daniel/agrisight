"""Pure HTML builders for the stakeholder website's visual layer.

Numbers shown here are passed in from verified aggregate bundles; nothing is
hard-coded. Pictures are original artwork (site_art) and never encode a value.
"""

from html import escape

from agrisight import site_art
from agrisight.public_evidence import CITATION
from agrisight.reporting_visuals import _image, svg

# Hero slideshow: the activities the survey asks about, in the order of its questions.
SLIDES = (("crops", "Crop farming"), ("livestock", "Livestock & poultry"),
          ("fish_farming", "Fish farming"), ("irrigation", "Water for crops"),
          ("market", "Harvest & markets"), ("fish_capture", "Fish capture"))

# Mosaic colours: coloured blocks >= 3.6:1 on the cream card; "Neither" is a labelled neutral.
BOTH, CROPS_ONLY, LIVESTOCK_ONLY, NEITHER = "#174d36", "#5b9341", "#b07a1c", "#d5dccb"


def pct(value: float | None, digits: int = 1) -> str:
    return "Undefined" if value is None else f"{100*value:.{digits}f}%"


def hero(households: int | None = None) -> str:
    """Crossfading illustrated slideshow; CSS-only and paused for reduced motion."""
    slides = "".join(
        f'<figure class="agri-slide" style="--i:{i}">{site_art.scene(name, "agri-slide-art")}'
        f'<figcaption>{escape(label)}</figcaption></figure>'
        for i, (name, label) in enumerate(SLIDES))
    dots = "".join(f'<i style="--i:{i}"></i>' for i in range(len(SLIDES)))
    reach = (f"what {households:,} surveyed households reported" if households
             else "what surveyed households reported")
    return ('<section class="agri-hero2" aria-label="AgriSight">'
            f'<div class="agri-slides" style="--n:{len(SLIDES)}">{slides}</div>'
            '<div class="agri-hero2-copy"><span class="agri-eyebrow">Agricultural data intelligence</span>'
            "<h1>Nigerian agriculture, <em>in evidence.</em></h1>"
            f'<p>Crops, livestock, fish, water, seeds and markets: {escape(reach)} '
            'in the National Agricultural Sample Survey, presented clearly and checked to the last number.</p>'
            f'</div><div class="agri-dots" aria-hidden="true">{dots}</div></section>')


def figures(items: list[tuple[str, str, str]]) -> str:
    """Key-figure band: (value, label, detail). Missing optional evidence is simply omitted."""
    cells = "".join(f'<li><strong>{escape(v)}</strong><span>{escape(label)}</span>'
                    f'<small>{escape(detail)}</small></li>' for v, label, detail in items)
    return f'<ul class="agri-figures">{cells}</ul>'


def heading(eyebrow: str, title: str, lead: str = "", centre: bool = False) -> str:
    lead_html = f"<p>{escape(lead)}</p>" if lead else ""
    css = "agri-heading agri-centre" if centre else "agri-heading"
    return f'<div class="{css}"><span>{escape(eyebrow)}</span><h2>{escape(title)}</h2>{lead_html}</div>'


def activity_cards(activities: list[dict]) -> str:
    """One illustrated card per activity: share, a to-scale bar and the counts behind it."""
    cards = []
    for a in activities:
        share = a["share"]
        bar = ('<div class="agri-card-bar" role="presentation"><div style="width:'
               f'{100*share:.4f}%"></div></div>' if share is not None else
               '<p class="agri-undefined-note">No valid responses: share undefined.</p>')
        cards.append(
            f'<article class="agri-activity-card">{site_art.scene(a["id"], "agri-card-art", True)}'
            f'<div class="agri-card-body"><h3>{escape(a["label"])}</h3>'
            f'<strong>{pct(share)}</strong>{bar}'
            f'<p>{a["yes"]:,} of {a["denominator"]:,} households with a valid answer</p>'
            f'<small>{escape(a["period"])}</small></div></article>')
    return f'<div class="agri-activity-cards">{"".join(cards)}</div>'


def overlap_mosaic(overlap: dict) -> str:
    """Area-true mosaic: column width = crop answer, height within column = livestock answer."""
    cells = {(c["crops"], c["livestock"]): c["count"] for c in overlap["cells"]}
    total = overlap["denominator"]
    if not total:
        return ('<div class="agri-mosaic agri-undefined"><p>No household answered both questions, '
                'so the overlap is undefined.</p></div>')
    W, H, gap = 520, 300, 3
    crops_yes = cells["yes", "yes"] + cells["yes", "no"]
    x_split = W * crops_yes / total
    rects = []
    for column, x0, width in (("yes", 0, x_split), ("no", x_split, W - x_split)):
        column_total = cells[column, "yes"] + cells[column, "no"]
        if not column_total or width <= 0:
            continue
        top = H * cells[column, "yes"] / column_total
        for livestock, y0, height in (("yes", 0, top), ("no", top, H - top)):
            colour = {("yes", "yes"): BOTH, ("yes", "no"): CROPS_ONLY,
                      ("no", "yes"): LIVESTOCK_ONLY, ("no", "no"): NEITHER}[column, livestock]
            if height > 0:
                rects.append(f'<rect x="{x0+gap/2:.2f}" y="{y0+gap/2:.2f}" width="{max(width-gap, .5):.2f}" '
                             f'height="{max(height-gap, .5):.2f}" rx="4" fill="{colour}"/>')
    rows = [("yes", "yes", BOTH, "Crops and livestock"), ("yes", "no", CROPS_ONLY, "Crops only"),
            ("no", "yes", LIVESTOCK_ONLY, "Livestock only"), ("no", "no", NEITHER, "Neither")]
    legend = "".join(
        f'<li><i style="background:{colour}"></i><span>{label}</span>'
        f'<b>{pct(cells[c, l]/total)}</b><small>{cells[c, l]:,} households</small></li>'
        for c, l, colour, label in rows)
    alt = "; ".join(f"{label}: {cells[c, l]:,} households ({pct(cells[c, l]/total)})"
                    for c, l, _, label in rows)
    art = _image(svg(f"0 0 {W} {H}", "".join(rects)), f"Mosaic of {total:,} households. {alt}.")
    return (f'<figure class="agri-mosaic"><div class="agri-mosaic-art">{art}'
            '<div class="agri-mosaic-axis"><span>Grew main-season crops →</span></div></div>'
            f'<figcaption><ul>{legend}</ul><p>Each block\'s area is its share of {total:,} households '
            'that answered both questions. Width splits households by crops; height splits each '
            'column by livestock or poultry.</p></figcaption></figure>')


def banner(eyebrow: str, title: str, lead: str, scene: str, compact: bool = False) -> str:
    """Inner-page banner: copy left, artwork right. Compact keeps charts near the top."""
    css = "agri-banner2 agri-compact" if compact else "agri-banner2"
    return (f'<section class="{css}"><div class="agri-banner2-copy"><span>{escape(eyebrow)}</span>'
            f'<h1>{escape(title)}</h1><p>{escape(lead)}</p></div>'
            f'<div class="agri-banner2-art">{site_art.scene(scene, "agri-banner-scene", True)}</div></section>')


def topic_card(scene: str, title: str, lead: str) -> str:
    return (f'<div class="agri-topic">{site_art.scene(scene, "agri-topic-art", True)}'
            f'<h3>{escape(title)}</h3><p>{escape(lead)}</p></div>')


def steps(items: list[tuple[str, str]]) -> str:
    cells = "".join(f'<li><b>{n:02d}</b><h3>{escape(t)}</h3><p>{escape(body)}</p></li>'
                    for n, (t, body) in enumerate(items, 1))
    return f'<ol class="agri-steps2">{cells}</ol>'


def footer(scope: str) -> str:
    return ('<footer class="agri-footer2"><div><div class="agri-wordmark">Agri<span>Sight</span></div>'
            '<p>Agricultural data intelligence and decision support.</p></div>'
            f'<div><b>Data source</b><p>{escape(scope)}</p><p>{escape(CITATION)}</p>'
            '<p><a href="https://microdata.nigerianstat.gov.ng/index.php/catalog/173" target="_blank" '
            'rel="noopener">NBS microdata catalogue</a></p></div>'
            '<div><b>About this site</b><p>Analysis and presentation by AgriSight; not an official NBS '
            'publication. NBS survey microdata are not redistributed.</p>'
            '<p>Illustrations are original AgriSight artwork.</p></div></footer>')
