"""Local, packaged presentation assets; decorative imagery is not survey evidence."""

import base64
from functools import lru_cache
from html import escape
from importlib.resources import files

import streamlit as st

IMAGE_CREDIT = "Illustration: AI-generated agricultural artwork."


@lru_cache(maxsize=1)
def presentation_assets() -> tuple[str, str]:
    assets = files("agrisight").joinpath("assets")
    css = assets.joinpath("dashboard.css").read_text(encoding="utf-8")
    image = base64.b64encode(assets.joinpath(
        "agricultural-landscape-v1.webp").read_bytes()).decode("ascii")
    return css, image


def styles() -> None:
    css, _ = presentation_assets()
    st.html(f"<style>{css}</style>")


def navigation(pages: tuple[str, ...], current: str, go) -> None:
    """Website-style top bar; the sidebar radio remains an equivalent fallback."""
    with st.container(horizontal=True, vertical_alignment="center", key="agri_topbar"):
        st.html('<div class="agri-wordmark">Agri<span>Sight</span></div>', width="content")
        with st.container(horizontal=True, horizontal_alignment="right", key="agri_nav",
                          gap="small"):
            for index, page in enumerate(pages):
                st.button(page, key=f"nav_{index}", on_click=go, args=(page,),
                          type="primary" if page == current else "tertiary")


def hero(eyebrow: str) -> None:
    _, image = presentation_assets()
    st.html(
        '<section class="agri-hero" aria-label="AgriSight agricultural intelligence">'
        f'<img src="data:image/webp;base64,{image}" alt="" />'
        f'<div class="agri-eyebrow">{escape(eyebrow)}</div>'
        '<h1>Farming evidence,<br>clearly told.</h1>'
        '<p>What agricultural households reported in a national agricultural survey, '
        'turned into findings you can read at a glance and check to the last number.</p>'
        '</section>')


def section(view: str, number: int) -> None:
    st.markdown(f'<div class="agri-section"><span>{number:02d}</span>'
                f'<b>{escape(view)}</b></div>', unsafe_allow_html=True)


def sidebar() -> None:
    st.sidebar.markdown(
        '<div class="agri-brand">Agri<span>Sight</span>'
        '<small>AGRICULTURAL INTELLIGENCE</small></div>'
        '<p class="agri-nav-label">Explore AgriSight</p>', unsafe_allow_html=True)


def footer() -> None:
    st.html('<footer class="agri-footer"><div><div class="agri-wordmark">Agri<span>Sight</span>'
            '</div><p>Agricultural intelligence, with the evidence in view.</p></div>'
            '<div><b>About the data</b><p>Survey findings and synthetic engineering studies '
            'are kept separate. Read-only research prototype.</p></div>'
            f'<div><b>Image credit</b><p>{IMAGE_CREDIT}</p></div></footer>')
