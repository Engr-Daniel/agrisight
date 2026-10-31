"""Accessible activity bars; controls and interpretation live in the product page."""

from html import escape

COLOURS = {"crops": "#174d36", "livestock": "#357047", "fish_capture": "#51813a",
           "fish_farming": "#647b35"}
ORDER = ("crops", "livestock", "fish_capture", "fish_farming")


def chart(activities: list[dict], unit: str) -> str:
    """Use a common zero baseline; undefined percentages are never painted as zero."""
    maximum = 100 if unit == "Percentages" else max((a["input_rows"] for a in activities), default=0)
    rows = []
    for item in sorted(activities, key=lambda a: ORDER.index(a["id"])):
        value = item["share"] * 100 if unit == "Percentages" and item["share"] is not None else (
            None if unit == "Percentages" else item["yes"])
        label = "Undefined" if value is None else f"{value:.2f}%" if unit == "Percentages" else f"{value:,}"
        width = value / maximum * 100 if value is not None and maximum else 0
        detail = (f'{item["yes"]:,} yes / {item["denominator"]:,} valid responses; '
                  f'{item["period"]}')
        rows.append('<li class="agri-activity-row" tabindex="0"><div class="agri-activity-label">'
                    f'<span>{escape(item["label"])}</span><strong>{label}</strong></div>'
                    f'<div class="agri-activity-track"><div style="width:{width:.8f}%;'
                    f'background:{COLOURS[item["id"]]}"></div></div>'
                    f'<small>{escape(detail)}</small></li>')
    scale = "100% of valid responses" if unit == "Percentages" else f"{maximum:,} household records"
    return ('<figure class="agri-activity-chart" aria-label="Reported agricultural activities">'
            '<ol>' + ''.join(rows) + '</ol><figcaption>Common scale: 0 to ' + scale +
            '. Hover over, focus or tap a bar for its counts and period. '
            'Undefined percentages have no bar.</figcaption></figure>')
