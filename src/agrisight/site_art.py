"""Original vector scenes for the AgriSight website.

The scenes illustrate the kinds of farming the survey asks about (crops, livestock,
fish, water, seeds, inputs, land, harvest and markets). They are drawn artwork: no
scene encodes a survey value, place or person. Each scene is a deterministic SVG
delivered as an <img> data URI, because Streamlit's HTML sanitiser strips inline SVG.
"""

from functools import cache

from agrisight.reporting_visuals import _image, svg

W, H = 960, 480

# Brand palette shared with dashboard.css.
SKY_TOP, SKY_LOW, SUN = "#f7e3b5", "#eaf1dc", "#f2bf4f"
HILL_FAR, HILL_MID, GROUND = "#b7cd98", "#86ad68", "#6d9a4e"
FOREST, LEAF, LIGHT_LEAF, DARK_LEAF = "#174d36", "#3f7d4a", "#8fbb69", "#2b6338"
SOIL, DARK_SOIL, PATH = "#a9764b", "#7b5233", "#dcc08f"
WATER, WATER_LIGHT, WATER_DEEP = "#5ba6b6", "#a5d3d9", "#3b7f92"
SKIN = ("#8a5636", "#6b3f27", "#9c6643")
WHEAT, CLAY, INDIGO, CLOTH = "#e3c77d", "#c8643b", "#2f4a7a", "#f6f1e3"


def _g(body: str, x: float = 0, y: float = 0, s: float = 1, flip: bool = False) -> str:
    sx = -s if flip else s
    return f'<g transform="translate({x:g} {y:g}) scale({sx:g} {s:g})">{body}</g>'


def sky(top: str = SKY_TOP, low: str = SKY_LOW) -> str:
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{low}"/>'
            f'</linearGradient></defs><rect width="{W}" height="{H}" fill="url(#sky)"/>')


def sun(cx: float, cy: float, r: float = 46) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*1.6:g}" fill="{SUN}" opacity=".18"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>')


def cloud(x: float, y: float, s: float = 1, colour: str = "#ffffff", opacity: float = .85) -> str:
    return _g(f'<g fill="{colour}" opacity="{opacity}"><ellipse cx="0" cy="0" rx="46" ry="16"/>'
              '<circle cx="-16" cy="-10" r="18"/><circle cx="12" cy="-16" r="22"/></g>', x, y, s)


def hills(far: str = HILL_FAR, mid: str = HILL_MID, ground: str = GROUND, line: int = 300) -> str:
    return (f'<path d="M0 {line-90} C160 {line-170} 300 {line-120} 430 {line-150} '
            f'S700 {line-200} 960 {line-120} V{H} H0Z" fill="{far}"/>'
            f'<path d="M0 {line-30} C200 {line-90} 380 {line-40} 560 {line-70} '
            f'S820 {line-110} 960 {line-60} V{H} H0Z" fill="{mid}"/>'
            f'<path d="M0 {line} C260 {line-30} 620 {line+10} 960 {line-20} V{H} H0Z" '
            f'fill="{ground}"/>')


def tree(x: float, y: float, s: float = 1, canopy: str = DARK_LEAF) -> str:
    """Broad savanna shade tree."""
    return _g(f'<path d="M-5 0 L-3 -60 Q-20 -70 -34 -66 M3 -60 L5 0 M0 -58 Q16 -72 30 -70" '
              f'stroke="{DARK_SOIL}" stroke-width="7" fill="none" stroke-linecap="round"/>'
              f'<rect x="-6" y="-62" width="12" height="62" rx="5" fill="{DARK_SOIL}"/>'
              f'<g fill="{canopy}"><ellipse cx="0" cy="-82" rx="70" ry="24"/>'
              f'<ellipse cx="-34" cy="-74" rx="36" ry="16"/><ellipse cx="36" cy="-76" rx="38" ry="17"/>'
              f'</g><ellipse cx="-10" cy="-92" rx="42" ry="10" fill="{LIGHT_LEAF}" opacity=".35"/>',
              x, y, s)


def palm(x: float, y: float, s: float = 1) -> str:
    fronds = "".join(f'<path d="M0 -120 Q{dx*.5:g} {-140+dy*.4:g} {dx} {-120+dy}" stroke="{LEAF}" '
                     'stroke-width="9" fill="none" stroke-linecap="round"/>'
                     for dx, dy in ((-60, 10), (60, 10), (-46, 34), (46, 34), (-20, -18), (24, -16)))
    return _g(f'<path d="M-4 0 Q-10 -60 0 -120 L6 -120 Q0 -60 6 0Z" fill="{DARK_SOIL}"/>{fronds}',
              x, y, s)


def house(x: float, y: float, s: float = 1, wall: str = "#d9a877") -> str:
    """Rural homestead: rendered walls and corrugated roof."""
    return _g(f'<rect x="-60" y="-56" width="120" height="56" fill="{wall}"/>'
              '<path d="M-72 -54 L-50 -86 H50 L72 -54Z" fill="#9aa4a6"/>'
              '<path d="M-60 -82 V-56 M-40 -86 V-54 M-20 -86 V-54 M0 -86 V-54 M20 -86 V-54 '
              'M40 -86 V-54" stroke="#7f898c" stroke-width="2"/>'
              f'<rect x="-14" y="-36" width="22" height="36" fill="{DARK_SOIL}"/>'
              '<rect x="24" y="-40" width="22" height="16" fill="#5a3b25"/>', x, y, s)


def granary(x: float, y: float, s: float = 1) -> str:
    return _g(f'<rect x="-22" y="-10" width="6" height="10" fill="{DARK_SOIL}"/>'
              f'<rect x="16" y="-10" width="6" height="10" fill="{DARK_SOIL}"/>'
              '<path d="M-26 -10 Q-30 -46 0 -50 Q30 -46 26 -10Z" fill="#c9915c"/>'
              f'<path d="M-36 -46 L0 -86 L36 -46Z" fill="{WHEAT}"/>'
              '<path d="M-24 -54 L0 -80 M0 -80 L24 -54 M-10 -50 L0 -80 L10 -50" stroke="#c7a75d" '
              'stroke-width="2" fill="none"/>', x, y, s)


def person(x: float, y: float, s: float = 1, skin: str = SKIN[0], top: str = CLAY,
           bottom: str = INDIGO, head: str = "hat", tool: str = "", flip: bool = False,
           skirt: bool = False) -> str:
    """Stylised farmer standing on (x, y). Tools: hoe, basket, staff, can, feed, tablet, net."""
    legs = (f'<path d="M-14 -50 L-17 0 H17 L14 -50Z" fill="{bottom}"/>' if skirt else
            f'<rect x="-11" y="-50" width="9" height="50" rx="3" fill="{bottom}"/>'
            f'<rect x="2" y="-50" width="9" height="50" rx="3" fill="{bottom}"/>')
    feet = '<ellipse cx="-8" cy="0" rx="8" ry="3" fill="#3b2a1d"/><ellipse cx="8" cy="0" rx="8" ry="3" fill="#3b2a1d"/>'
    body = f'<path d="M-15 -48 L-13 -90 Q0 -98 13 -90 L15 -48Z" fill="{top}"/>'
    face = f'<rect x="-4" y="-100" width="8" height="8" fill="{skin}"/><circle cy="-108" r="11" fill="{skin}"/>'
    hats = {
        "hat": (f'<ellipse cy="-114" rx="22" ry="5" fill="{WHEAT}"/>'
                f'<path d="M-11 -114 Q0 -132 11 -114Z" fill="{WHEAT}"/>'
                '<path d="M-11 -116 H11" stroke="#b58f3d" stroke-width="2"/>'),
        "wrap": f'<path d="M-13 -110 Q-14 -128 2 -126 Q16 -126 14 -110 Q0 -116 -13 -110Z" fill="{top}"/>'
                f'<path d="M8 -126 Q20 -132 18 -120" stroke="{top}" stroke-width="5" fill="none"/>',
        "cap": f'<path d="M-11 -112 Q0 -126 11 -112Z" fill="{INDIGO}"/><rect x="6" y="-114" width="12" height="3" fill="{INDIGO}"/>',
        "": "",
    }
    near = f'stroke="{skin}" stroke-width="7" stroke-linecap="round" fill="none"'
    arms = {
        "hoe": (f'<path d="M-10 -86 L4 -64 L22 -70" {near}/><path d="M10 -86 L24 -68" {near}/>'
                f'<path d="M14 -92 L48 -6" stroke="{DARK_SOIL}" stroke-width="5" stroke-linecap="round"/>'
                '<path d="M46 -8 L62 -2 L56 6 L42 0Z" fill="#6e7275"/>'),
        "basket": (f'<path d="M-10 -86 L-18 -112" {near}/><path d="M10 -86 L18 -112" {near}/>'
                   '<path d="M-26 -118 H26 L20 -136 H-20Z" fill="#c58b47"/>'
                   '<path d="M-22 -126 H22" stroke="#9b6a32" stroke-width="2"/>'
                   '<circle cx="-10" cy="-140" r="7" fill="#e3a53a"/><circle cx="4" cy="-142" r="8" fill="#d9822b"/>'
                   '<circle cx="14" cy="-138" r="6" fill="#f0c04e"/>'),
        "staff": (f'<path d="M-10 -86 L-16 -52" {near}/><path d="M10 -86 L24 -70" {near}/>'
                  f'<path d="M26 -124 L26 0" stroke="{DARK_SOIL}" stroke-width="5" stroke-linecap="round"/>'),
        "can": (f'<path d="M-10 -86 L-16 -52" {near}/><path d="M10 -86 L20 -60" {near}/>'
                '<path d="M12 -62 h22 v22 h-22z" fill="#7d9aa1"/><path d="M34 -56 L52 -66" stroke="#7d9aa1" stroke-width="5"/>'
                f'<path d="M56 -64 q6 10 2 22 M60 -62 q8 12 6 24" stroke="{WATER_LIGHT}" stroke-width="2" fill="none"/>'),
        "feed": (f'<path d="M-10 -86 L-18 -60" {near}/><path d="M10 -86 L30 -78" {near}/>'
                 '<path d="M-28 -62 h22 l-3 18 h-16z" fill="#b98b4f"/>'
                 '<g fill="#e6cf8f"><circle cx="38" cy="-70" r="2"/><circle cx="44" cy="-60" r="2"/>'
                 '<circle cx="40" cy="-50" r="2"/><circle cx="48" cy="-44" r="2"/></g>'),
        "tablet": (f'<path d="M-10 -86 L-2 -66 L12 -70" {near}/><path d="M10 -86 L16 -70" {near}/>'
                   '<rect x="6" y="-82" width="20" height="26" rx="3" fill="#2d3a40"/>'
                   '<rect x="9" y="-79" width="14" height="19" rx="1" fill="#a9d3c2"/>'),
        "net": (f'<path d="M-10 -86 L-20 -66" {near}/><path d="M10 -86 L26 -96" {near}/>'
                f'<path d="M26 -96 Q60 -110 70 -70 Q50 -54 26 -96Z" fill="none" stroke="{CLOTH}" stroke-width="2"/>'
                f'<path d="M34 -98 L56 -62 M46 -102 L64 -66 M30 -88 L68 -84" stroke="{CLOTH}" stroke-width="1.4"/>'),
        "": f'<path d="M-10 -86 L-16 -52" {near}/><path d="M10 -86 L16 -52" {near}/>',
    }
    return _g(legs + feet + body + face + hats[head] + arms[tool], x, y, s, flip)


def cow(x: float, y: float, s: float = 1, coat: str = "#efe6d6", patch: str = "#b9a58c",
        flip: bool = False) -> str:
    """Zebu cattle, the humped breed common in Nigerian herds."""
    leg = coat if coat != "#efe6d6" else "#d8ccb7"
    legs = "".join(f'<rect x="{lx}" y="-34" width="9" height="34" rx="3" fill="{leg}"/>'
                   for lx in (-40, -26, 22, 34))
    return _g(f'{legs}<ellipse cx="0" cy="-48" rx="50" ry="23" fill="{coat}"/>'
              f'<ellipse cx="-14" cy="-52" rx="16" ry="11" fill="{patch}" opacity=".7"/>'
              f'<path d="M18 -66 Q28 -92 42 -68Z" fill="{coat}"/>'
              f'<path d="M40 -60 Q58 -70 70 -58 L72 -36 Q62 -30 56 -40 Q48 -44 40 -46Z" fill="{coat}"/>'
              f'<path d="M44 -44 Q48 -24 40 -24" fill="{coat}"/>'
              '<path d="M60 -64 Q56 -84 66 -88 M66 -64 Q72 -82 82 -84" stroke="#d6c7a6" stroke-width="4" '
              'fill="none" stroke-linecap="round"/>'
              '<circle cx="64" cy="-54" r="2.4" fill="#2d241c"/>'
              '<ellipse cx="70" cy="-38" rx="5" ry="4" fill="#cdb79c"/>'
              f'<path d="M-50 -52 Q-62 -40 -58 -18" stroke="{coat}" stroke-width="3" fill="none"/>'
              '<path d="M-60 -20 l-3 8 l7 -3z" fill="#5a4636"/>', x, y, s, flip)


def goat(x: float, y: float, s: float = 1, coat: str = "#d9c9ad", flip: bool = False) -> str:
    legs = "".join(f'<rect x="{lx}" y="-22" width="5" height="22" rx="2" fill="{coat}"/>'
                   for lx in (-20, -12, 12, 18))
    return _g(f'{legs}<ellipse cx="0" cy="-30" rx="26" ry="13" fill="{coat}"/>'
              f'<path d="M20 -36 L30 -54 L42 -48 L36 -34Z" fill="{coat}"/>'
              '<path d="M30 -54 Q26 -66 18 -64 M34 -54 Q32 -68 24 -70" stroke="#8f7c5e" stroke-width="3" fill="none"/>'
              '<path d="M38 -36 l2 8" stroke="#8f7c5e" stroke-width="2"/>'
              '<circle cx="35" cy="-48" r="1.8" fill="#2d241c"/>'
              f'<path d="M-25 -34 l-8 -8" stroke="{coat}" stroke-width="4" stroke-linecap="round"/>',
              x, y, s, flip)


def chicken(x: float, y: float, s: float = 1, feather: str = "#f4efe4", flip: bool = False) -> str:
    return _g(f'<path d="M-2 -4 V0 M4 -4 V0" stroke="#d58c2c" stroke-width="2"/>'
              f'<ellipse cx="0" cy="-14" rx="13" ry="10" fill="{feather}"/>'
              f'<path d="M-10 -18 Q-22 -32 -14 -12Z" fill="{feather}"/>'
              f'<circle cx="10" cy="-26" r="7" fill="{feather}"/>'
              '<path d="M8 -33 q3 -5 6 0 q2 -4 4 1" fill="#c8402f"/>'
              '<path d="M17 -26 l6 2 l-6 2z" fill="#e2a23a"/><circle cx="12" cy="-27" r="1.3" fill="#222"/>',
              x, y, s, flip)


def fish(x: float, y: float, s: float = 1, colour: str = "#d98a47", flip: bool = False,
         opacity: float = 1) -> str:
    return _g(f'<g opacity="{opacity:g}"><path d="M-22 0 Q0 -14 22 0 Q0 14 -22 0Z" fill="{colour}"/>'
              f'<path d="M-20 0 L-34 -10 L-32 10Z" fill="{colour}"/>'
              '<circle cx="12" cy="-2" r="2" fill="#1f2a2e"/>'
              '<path d="M0 -8 Q4 0 0 8" stroke="#ffffff" stroke-opacity=".35" stroke-width="2" fill="none"/></g>',
              x, y, s, flip)


def maize(x: float, y: float, s: float = 1) -> str:
    return _g(f'<path d="M0 0 V-92" stroke="{LEAF}" stroke-width="4"/>'
              f'<path d="M0 -30 Q-26 -44 -34 -30 M0 -48 Q26 -64 36 -48 M0 -66 Q-22 -86 -30 -74 '
              f'M0 -80 Q18 -98 26 -90" stroke="{LEAF}" stroke-width="5" fill="none" stroke-linecap="round"/>'
              f'<ellipse cx="6" cy="-56" rx="5" ry="11" fill="{WHEAT}"/>'
              '<path d="M0 -92 l-6 -12 M0 -92 l6 -12 M0 -92 v-14" stroke="#c9a54f" stroke-width="2"/>',
              x, y, s)


def leafy(x: float, y: float, s: float = 1, colour: str = LEAF) -> str:
    """Low leafy crop such as cassava, cowpea or vegetables."""
    return _g(f'<g fill="{colour}"><ellipse cx="-12" cy="-12" rx="14" ry="7" transform="rotate(-30 -12 -12)"/>'
              '<ellipse cx="12" cy="-12" rx="14" ry="7" transform="rotate(30 12 -12)"/>'
              '<ellipse cx="0" cy="-22" rx="7" ry="14"/></g>'
              f'<path d="M0 0 V-14" stroke="{DARK_LEAF}" stroke-width="2"/>', x, y, s)


def yam_mound(x: float, y: float, s: float = 1) -> str:
    return _g(f'<path d="M-26 0 Q0 -30 26 0Z" fill="{SOIL}"/>'
              f'<path d="M0 -16 Q-6 -46 6 -66" stroke="{DARK_LEAF}" stroke-width="2" fill="none"/>'
              f'<g fill="{LEAF}"><path d="M2 -40 q12 -10 16 2 q-10 6 -16 -2z"/>'
              '<path d="M-2 -54 q-12 -10 -16 2 q10 6 16 -2z"/></g>', x, y, s)


def crop_rows(y0: float, rows: int, plant, spacing: float = 54, start: float = -20,
              end: float = W + 20, scale0: float = .55, scale1: float = 1.1, gap: float = 32) -> str:
    """Rows of plants receding into the distance (smaller and higher further away)."""
    out = []
    for r in range(rows):
        t = r / max(rows-1, 1)
        s = scale0 + (scale1-scale0)*t
        y = y0 + gap*r*(0.6+0.8*t)
        step = spacing*s
        n = int((end-start)/step)+1
        offset = (r % 2)*step/2
        out.extend(plant(start+offset+i*step, y, s) for i in range(n))
    return "".join(out)


def soil_bands(y0: float, rows: int, gap: float = 32, colour: str = SOIL) -> str:
    out = []
    for r in range(rows):
        t = r / max(rows-1, 1)
        y = y0 + gap*r*(0.6+0.8*t)
        out.append(f'<path d="M-20 {y:.1f} Q480 {y-8:.1f} 980 {y:.1f}" stroke="{colour}" '
                   f'stroke-width="{4+8*t:.1f}" stroke-opacity=".55" fill="none"/>')
    return "".join(out)


def pond(cx: float, cy: float, rx: float, ry: float) -> str:
    ripples = "".join(f'<ellipse cx="{cx+dx}" cy="{cy+dy}" rx="{r}" ry="{r*.32:.1f}" fill="none" '
                      f'stroke="#ffffff" stroke-opacity=".45" stroke-width="2"/>'
                      for dx, dy, r in ((-rx*.35, -ry*.2, 26), (rx*.3, ry*.15, 34), (rx*.05, -ry*.45, 18)))
    return (f'<ellipse cx="{cx}" cy="{cy+8}" rx="{rx+14}" ry="{ry+10}" fill="#7d6a45"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WATER}"/>'
            f'<ellipse cx="{cx}" cy="{cy+ry*.2:.1f}" rx="{rx*.8:.1f}" ry="{ry*.6:.1f}" fill="{WATER_DEEP}" opacity=".35"/>'
            + ripples)


def reeds(x: float, y: float, s: float = 1) -> str:
    return _g(f'<g stroke="{DARK_LEAF}" stroke-width="3" fill="none" stroke-linecap="round">'
              '<path d="M0 0 Q-4 -30 -10 -50"/><path d="M6 0 Q8 -36 4 -60"/><path d="M12 0 Q18 -24 26 -42"/></g>'
              '<rect x="1" y="-66" width="6" height="16" rx="3" fill="#7b5233"/>', x, y, s)


def sack(x: float, y: float, s: float = 1, colour: str = "#efe4c8", band: str = LEAF,
         label: str = "") -> str:
    mark = (f'<text x="0" y="-26" text-anchor="middle" font-family="sans-serif" font-weight="700" '
            f'font-size="11" fill="{band}">{label}</text>' if label else "")
    return _g(f'<path d="M-24 0 Q-28 -40 -20 -58 H20 Q28 -40 24 0Z" fill="{colour}"/>'
              f'<path d="M-20 -58 Q0 -66 20 -58" stroke="#c9b98e" stroke-width="3" fill="none"/>'
              f'<rect x="-22" y="-40" width="44" height="8" fill="{band}" opacity=".85"/>{mark}', x, y, s)


def scene_crops() -> str:
    return (sky() + sun(780, 110) + cloud(200, 90) + cloud(560, 70, .7) + hills()
            + house(150, 270, .7) + granary(240, 272, .7) + palm(84, 280, .7) + tree(860, 290, .9)
            + soil_bands(300, 6, 34) + crop_rows(296, 6, maize, spacing=62)
            + person(600, 455, 1.15, SKIN[0], CLAY, INDIGO, "hat", "hoe")
            + person(760, 440, 1.05, SKIN[1], "#e3a53a", "#4b6a3a", "wrap", "basket", skirt=True))


def scene_livestock() -> str:
    return (sky("#f5dfae", "#eef1dc") + sun(160, 110, 40) + cloud(700, 80) + hills(line=310)
            + tree(820, 320, 1.1) + tree(120, 300, .7)
            + cow(420, 400, 1.15) + cow(610, 380, .95, "#8a5a3a", "#5e3c26", flip=True)
            + cow(250, 370, .75, "#e8dcc6", "#a4876a")
            + goat(720, 440, 1.1) + goat(820, 450, .9, "#6d5845", flip=True)
            + chicken(160, 450, 1.2) + chicken(210, 462, 1, "#c56b3b", flip=True) + chicken(110, 470, .9)
            + person(330, 470, 1.15, SKIN[1], "#f6f1e3", "#7b5233", "cap", "staff"))


def scene_fishpond() -> str:
    fishes = "".join(fish(x, y, s, c, f, .8) for x, y, s, c, f in (
        (380, 370, 1.2, "#e09a54", False), (500, 395, 1, "#c97a3e", True), (600, 360, .9, "#e8b56a", False),
        (450, 420, .8, "#d98a47", True), (690, 410, 1.1, "#e09a54", True)))
    return (sky("#f6e6bf", "#e4f0e3") + sun(820, 100, 38) + cloud(320, 80) + hills(line=280)
            + palm(90, 300, .9) + tree(870, 290, .8)
            + pond(530, 385, 300, 72) + fishes + reeds(250, 420) + reeds(820, 410, .9)
            + person(160, 465, 1.15, SKIN[2], INDIGO, "#4f4f4f", "cap", "feed")
            + person(880, 470, 1, SKIN[0], CLAY, INDIGO, "wrap", "net", flip=True, skirt=True))


def scene_fishing() -> str:
    canoe = ('<path d="M-130 -10 Q0 26 130 -10 L118 6 Q0 34 -118 6Z" fill="#7b5233"/>'
             '<path d="M-118 4 Q0 28 118 4" stroke="#5a3b25" stroke-width="3" fill="none"/>')
    waves = "".join(f'<path d="M{x} {y} q20 -8 40 0 t40 0" stroke="#ffffff" stroke-opacity=".5" '
                    'stroke-width="2" fill="none"/>' for x, y in ((80, 380), (300, 430), (620, 400), (760, 450)))
    return (sky("#f9dca6", "#e2eee4") + sun(480, 230, 60)
            + f'<path d="M0 250 C200 230 360 260 520 244 S800 236 960 252 V{H} H0Z" fill="{HILL_MID}"/>'
            + f'<rect y="290" width="{W}" height="190" fill="{WATER}"/>'
            + f'<rect y="290" width="{W}" height="14" fill="{WATER_LIGHT}" opacity=".6"/>'
            + waves + palm(70, 296, .8) + palm(900, 292, .7) + _g(canoe, 520, 392)
            + person(470, 384, .95, SKIN[1], "#e3a53a", INDIGO, "hat", "net")
            + person(600, 384, .9, SKIN[0], CLOTH, "#4b6a3a", "cap", "", flip=True)
            + fish(380, 450, .9, "#c9d4d6", opacity=.5) + fish(700, 460, .8, "#c9d4d6", True, .5))


def scene_irrigation() -> str:
    channel = (f'<path d="M500 300 C520 340 470 380 520 420 S600 470 620 {H}" stroke="{WATER}" '
               'stroke-width="26" fill="none"/>'
               f'<path d="M500 300 C520 340 470 380 520 420 S600 470 620 {H}" stroke="{WATER_LIGHT}" '
               'stroke-width="6" fill="none" stroke-dasharray="18 22"/>')
    sprinkler = ('<path d="M0 0 V-46" stroke="#5f6b6e" stroke-width="4"/>'
                 + "".join(f'<path d="M0 -46 Q{dx*.5:g} -90 {dx} -30" stroke="{WATER_LIGHT}" stroke-width="3" '
                           'fill="none" stroke-dasharray="4 7"/>' for dx in (-90, -50, 50, 90)))
    pump = (f'<rect x="-34" y="-40" width="68" height="40" rx="6" fill="{CLAY}"/>'
            '<circle cx="-12" cy="-20" r="10" fill="#3c3c3c"/><rect x="34" y="-28" width="40" height="10" fill="#5f6b6e"/>')
    return (sky() + sun(150, 100) + cloud(650, 80) + hills()
            + '<rect x="740" y="190" width="80" height="70" fill="#9aa4a6"/>'
            + '<path d="M730 190 h100 l-10 -20 h-80z" fill="#7f898c"/><path d="M760 260 v40 M800 260 v40" stroke="#7f898c" stroke-width="6"/>'
            + soil_bands(300, 6, 34) + crop_rows(296, 6, leafy, spacing=46, scale1=1.4)
            + channel + _g(sprinkler, 240, 400, 1.1) + _g(sprinkler, 780, 420, 1)
            + _g(pump, 430, 330, .9)
            + person(640, 460, 1.15, SKIN[2], "#4b6a3a", "#4f4f4f", "hat", "can"))


def scene_seeds() -> str:
    tray = "".join(f'<rect x="{x}" y="446" width="30" height="14" rx="2" fill="#6b4a2f"/>'
                   for x in range(60, 400, 36))
    seedlings = "".join(leafy(x+15, 448, .62, LIGHT_LEAF) for x in range(60, 400, 36))
    scatter = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#d9b25a"/>'
                      for x, y in ((610, 330), (624, 352), (598, 362), (640, 372), (612, 388), (650, 398)))
    return (sky("#f7e6bd", "#edf2dd") + sun(820, 110, 40) + cloud(300, 90) + hills(line=300)
            + soil_bands(300, 6, 34, DARK_SOIL)
            + crop_rows(296, 4, lambda x, y, s: leafy(x, y, s*.5, LIGHT_LEAF), spacing=40, scale1=1)
            + tray + seedlings + scatter
            + sack(760, 470, 1.6, label="SEED") + sack(860, 470, 1.3, "#e6d7b0", CLAY)
            + person(560, 470, 1.2, SKIN[1], LEAF, INDIGO, "wrap", "feed", skirt=True))


def scene_garden() -> str:
    """A kitchen garden behind a homestead, a cultivated plot and a fallow plot."""
    fence = "".join(f'<rect x="{x}" y="360" width="5" height="44" fill="#9b6a3c"/>' for x in range(40, 420, 28))
    fallow = "".join(f'<path d="M{x} {y} q4 -14 8 0" stroke="#a9a46a" stroke-width="2" fill="none"/>'
                     for x in range(520, 940, 34) for y in (330, 360, 392))
    return (sky() + sun(840, 96, 40) + cloud(500, 80) + hills(line=300)
            + house(200, 330, .9) + tree(420, 320, .7)
            + '<path d="M480 300 L960 290 V420 L470 430Z" fill="#c9b27a"/>' + fallow
            + soil_bands(410, 3, 26) + crop_rows(410, 3, maize, spacing=60, start=500, scale0=.6, scale1=.9, gap=26)
            + '<rect x="40" y="376" width="380" height="104" fill="#8a5f3b"/>'
            + crop_rows(400, 3, leafy, spacing=40, start=60, end=410, scale0=.8, scale1=1.1, gap=26)
            + '<path d="M40 362 H420 M40 384 H420" stroke="#9b6a3c" stroke-width="3"/>' + fence
            + chicken(470, 470, 1.1) + person(330, 470, 1.1, SKIN[2], CLAY, INDIGO, "wrap", "can", skirt=True))


def scene_inputs() -> str:
    sprayer = ('<rect x="-14" y="-96" width="22" height="34" rx="6" fill="#4f7fa8"/>'
               '<path d="M8 -70 Q40 -60 54 -40" stroke="#3c3c3c" stroke-width="3" fill="none"/>'
               f'<path d="M58 -40 q10 6 14 18 M60 -44 q14 2 22 12" stroke="{WATER_LIGHT}" stroke-width="2" fill="none" stroke-dasharray="3 4"/>')
    return (sky() + sun(170, 100, 40) + cloud(560, 80) + hills()
            + soil_bands(300, 6, 34) + crop_rows(296, 6, maize, spacing=66)
            + sack(130, 470, 1.4, label="NPK") + sack(220, 470, 1.25, "#f0e9d6", CLAY, "UREA")
            + sack(300, 470, 1.1, "#ece3cd", "#7b5233", "MANURE")
            + _g(person(0, 0, 1.15, SKIN[0], "#e3a53a", "#4b6a3a", "cap", "") + _g(sprayer, 0, 0, 1.15), 640, 465))


def scene_land() -> str:
    patches = (f'<path d="M0 300 L300 280 L360 360 L0 400Z" fill="#9bbf6c"/>'
               f'<path d="M300 280 L620 290 L640 370 L360 360Z" fill="#c7b46a"/>'
               f'<path d="M620 290 L960 284 V380 L640 370Z" fill="#7fae5a"/>'
               f'<path d="M0 400 L360 360 L400 {H} H0Z" fill="#b8925d"/>'
               f'<path d="M360 360 L640 370 L700 {H} H400Z" fill="#8fb862"/>'
               f'<path d="M640 370 L960 380 V{H} H700Z" fill="#c9a96a"/>')
    hedges = ('<path d="M0 300 L300 280 L620 290 L960 284 M0 400 L360 360 L640 370 L960 380 '
              f'M300 280 L360 360 L400 {H} M620 290 L640 370 L700 {H}" stroke="{DARK_LEAF}" stroke-width="5" '
              'fill="none" stroke-linecap="round" opacity=".7"/>')
    path = f'<path d="M210 {H} C260 420 300 380 330 340 S420 300 470 288" stroke="{PATH}" stroke-width="14" fill="none"/>'
    bike = ('<circle cx="-22" cy="-12" r="12" fill="none" stroke="#333" stroke-width="3"/>'
            '<circle cx="22" cy="-12" r="12" fill="none" stroke="#333" stroke-width="3"/>'
            f'<path d="M-22 -12 L-4 -34 L16 -34 L22 -12 M-4 -34 L4 -12 L-22 -12" stroke="{CLAY}" stroke-width="3" fill="none"/>')
    return (sky() + sun(830, 100, 40) + cloud(240, 90) + hills(line=290) + patches + hedges + path
            + house(500, 286, .55) + tree(120, 300, .6) + tree(880, 290, .7)
            + crop_rows(340, 2, maize, spacing=44, start=650, end=940, scale0=.5, scale1=.6, gap=20)
            + crop_rows(410, 2, yam_mound, spacing=60, start=20, end=330, scale0=.8, scale1=1, gap=28)
            + _g(bike, 300, 404, 1.1) + person(300, 392, .8, SKIN[1], INDIGO, "#4f4f4f", "cap", ""))


def scene_harvest() -> str:
    rain = "".join(f'<path d="M{x} {y} l-6 16" stroke="#7d9aa1" stroke-width="2"/>'
                   for x in range(700, 900, 22) for y in (120, 150))
    return (sky("#efe3c3", "#e8eedc") + cloud(780, 90, 1.5, "#9aa6a8", .9) + rain + sun(160, 110, 40)
            + hills(far="#c2c99a", mid="#a3b574") + soil_bands(300, 6, 34)
            + crop_rows(296, 3, maize, spacing=64, end=480) + crop_rows(296, 3, leafy, spacing=48, start=500)
            + '<g fill="#e7c25c"><ellipse cx="160" cy="440" rx="60" ry="18"/><ellipse cx="150" cy="424" rx="44" ry="14"/></g>'
            + person(330, 465, 1.15, SKIN[0], CLAY, INDIGO, "wrap", "basket", skirt=True)
            + person(560, 460, 1.1, SKIN[1], "#4b6a3a", "#5a4636", "hat", "hoe", flip=True))


def scene_market() -> str:
    stall = ('<rect x="-150" y="-120" width="8" height="120" fill="#7b5233"/><rect x="142" y="-120" width="8" height="120" fill="#7b5233"/>'
             + "".join(f'<path d="M{x} -150 h50 v34 q-25 14 -50 0z" fill="{c}"/>'
                       for x, c in zip(range(-160, 160, 50), (CLAY, CLOTH, CLAY, CLOTH, CLAY, CLOTH, CLAY), strict=False))
             + '<rect x="-150" y="-50" width="300" height="50" fill="#a9764b"/>')
    produce = "".join(
        f'<path d="M{x-30} -50 q30 18 60 0 l-6 -18 h-48z" fill="#c58b47"/>'
        + "".join(f'<circle cx="{x+dx}" cy="{-66+dy}" r="9" fill="{c}"/>' for dx, dy in ((-14, 0), (0, -6), (14, 0)))
        for x, c in ((-100, "#d6402f"), (-20, "#e3a53a"), (60, "#6b9a3a"), (120, "#c8643b")))
    yams = ('<g fill="#8a6142"><ellipse cx="-230" cy="-14" rx="34" ry="12" transform="rotate(-8 -230 -14)"/>'
            '<ellipse cx="-210" cy="-30" rx="30" ry="11" transform="rotate(10 -210 -30)"/></g>')
    return (sky("#f7e3b5", "#f1efe0") + sun(140, 100, 40) + cloud(560, 70) + hills(line=300, ground="#c9b27e")
            + granary(820, 330, 1.2) + house(700, 320, .7, "#e1c08f")
            + _g(stall + produce + yams, 440, 450)
            + person(250, 470, 1.15, SKIN[2], "#e3a53a", INDIGO, "wrap", "", skirt=True)
            + person(650, 470, 1.15, SKIN[0], CLOTH, "#4b6a3a", "cap", "basket", flip=True)
            + sack(880, 470, 1.2) + sack(930, 472, 1, "#e6d7b0", CLAY))


def scene_survey() -> str:
    """An interviewer recording a farmer's answers on a tablet under a shade tree."""
    return (sky() + sun(820, 100, 40) + cloud(420, 80) + hills()
            + soil_bands(330, 4, 34) + crop_rows(326, 4, leafy, spacing=50, start=560, scale1=1)
            + tree(330, 440, 1.8) + house(820, 320, .6)
            + '<rect x="190" y="420" width="70" height="10" rx="4" fill="#7b5233"/>'
            '<path d="M200 430 v30 M250 430 v30" stroke="#7b5233" stroke-width="6"/>'
            + person(230, 465, 1.15, SKIN[1], CLAY, INDIGO, "hat", "")
            + person(400, 465, 1.15, SKIN[0], "#4f7fa8", "#3b3b3b", "", "tablet", flip=True)
            + chicken(520, 470, 1) + goat(110, 470, .9))


SCENES = {
    "crops": (scene_crops, "Farmers tending a maize field beside a rural homestead."),
    "livestock": (scene_livestock, "A herder with zebu cattle, goats and chickens."),
    "fish_farming": (scene_fishpond, "A farmer feeding fish in an earthen pond."),
    "fish_capture": (scene_fishing, "Two people fishing with a net from a wooden canoe on a river."),
    "irrigation": (scene_irrigation, "An irrigation channel, pump and sprinklers watering crop rows."),
    "seeds": (scene_seeds, "A farmer sowing seed beside seedling trays and seed sacks."),
    "inputs": (scene_inputs, "Fertiliser and manure sacks beside a farmer spraying a maize field."),
    "garden": (scene_garden, "A kitchen garden beside a homestead, with cultivated and fallow plots."),
    "land": (scene_land, "A patchwork of farm plots reached by a path from a homestead."),
    "harvest": (scene_harvest, "Farmers harvesting crops while rain clouds gather."),
    "market": (scene_market, "A produce stall with baskets of crops beside a grain store."),
    "survey": (scene_survey, "An interviewer recording a farmer's answers under a shade tree."),
}


@cache
def drawing(name: str) -> str:
    builder, _ = SCENES[name]
    return svg(f"0 0 {W} {H}", builder()).replace(
        "<svg ", '<svg preserveAspectRatio="xMidYMid slice" ', 1)


def scene(name: str, css: str = "agri-scene", decorative: bool = False) -> str:
    """One illustrated scene as a sanitiser-safe <img>; alt text describes the artwork."""
    _, alt = SCENES[name]
    return _image(drawing(name), "" if decorative else alt, css)
