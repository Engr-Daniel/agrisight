"""Compact stakeholder context; detailed analytical contracts stay in the repository."""

import streamlit as st


def show(period: str, scope: str) -> None:
    """Keep the source, exact reference period and counting scope beside a finding."""
    st.caption(f"Data context · NBS NASS 2023 · {period} · {scope}")
