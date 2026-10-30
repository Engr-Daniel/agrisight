"""Local, packaged presentation assets; decorative imagery is not survey evidence."""

import base64
from functools import lru_cache
from html import escape
from importlib.resources import files

import streamlit as st


@lru_cache(maxsize=1)
def presentation_assets() -> tuple[str, str]:
    assets = files("agrisight").joinpath("assets")
    css = assets.joinpath("dashboard.css").read_text(encoding="utf-8")
    image = base64.b64encode(assets.joinpath(
        "agricultural-landscape-v1.webp").read_bytes()).decode("ascii")
    return css, image


def header(hero: bool = True) -> None:
    css, image = presentation_assets()
    st.html(f"<style>{css}</style>")
    st.html('<div class="agri-masthead"><span>AgriSight / Agricultural intelligence</span>'
            '<span class="agri-dot">Research &amp; decision support</span></div>')
    if not hero:
        return
    st.html(
        '<section class="agri-hero" aria-label="AgriSight agricultural intelligence">'
        f'<img src="data:image/webp;base64,{image}" alt="" />'
        '<div class="agri-eyebrow">Agricultural data intelligence</div>'
        '<h1>A clearer view<br>of agriculture.</h1>'
        '<p>Agricultural intelligence for better-informed decisions. '
        'Discover the findings, then explore the evidence behind them.</p></section>'
        '<p class="agri-art-note">AI-generated illustration · decorative, not survey imagery.</p>')


def sidebar() -> None:
    st.sidebar.markdown(
        '<div class="agri-brand">Agri<span>Sight</span>'
        '<small>AGRICULTURAL INTELLIGENCE</small></div>'
        '<p class="agri-nav-label">Explore AgriSight</p>', unsafe_allow_html=True)


def section(view: str, number: int) -> None:
    st.markdown(f'<div class="agri-section"><span>{number:02d}</span>'
                f'<b>{escape(view)}</b></div>', unsafe_allow_html=True)


def footer() -> None:
    st.markdown('<footer class="agri-footer"><strong>AgriSight</strong> · '
                'Agricultural intelligence, with evidence in view.<br>'
                'Read-only research explorer · Survey findings and synthetic experiments '
                'remain separate.</footer>', unsafe_allow_html=True)
