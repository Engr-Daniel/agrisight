"""Stakeholder questions, eligible responses and interpretation for irrigation."""

from html import escape

import pandas as pd
import streamlit as st

OPTIONS = ("Infrastructure presence", "Irrigation methods", "Water sources")


def rate(value: float | None) -> str:
    return "Undefined" if value is None else f"{100*value:.2f}%"


def bars(rows: list[dict], denominator: int, unit: str) -> str:
    body = []
    for row in rows:
        label = rate(row["share"]) if unit == "Percentages" else f'{row["count"]:,}'
        width = 100*row["count"]/denominator if denominator else 0
        body.append('<li class="agri-activity-row"><div class="agri-activity-label">'
                    f'<span>{escape(row["label"])}</span><strong>{label}</strong></div>'
                    f'<div class="agri-activity-track"><div style="width:{width:.8f}%;'
                    'background:#357047"></div></div></li>')
    maximum = "100%" if unit == "Percentages" else f"{denominator:,} plot responses"
    return '<figure class="agri-activity-chart agri-water-chart"><ol>' + ''.join(body) + (
        f'</ol><figcaption>Common scale: 0 to {maximum}. Undefined shares have no bar.</figcaption></figure>')


def show(bundle: dict) -> None:
    st.subheader("Water Management")
    st.write("What irrigation infrastructure is reported, and which main methods and water sources "
             "do infrastructure-yes plots report?")
    if bundle["status"] != "available":
        st.info("Reviewed irrigation evidence is unavailable. Water Management findings are hidden; "
                "other agricultural findings remain available.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative irrigation records, not survey findings.")
    selection = st.selectbox("Explore water management", OPTIONS, key="water_question")
    unit = st.radio("Show water-management values as", ("Percentages", "Plot counts"),
                    horizontal=True, key="water_unit")
    presence = bundle["infrastructure"]
    if selection == OPTIONS[0]:
        selected = presence
        denominator = presence["denominator"]
        eligible = presence["input_rows"]
        rows = [{"label": label, "count": presence[key],
                 "share": presence[key]/denominator if denominator else None}
                for key, label in (("yes", "Infrastructure reported"), ("no", "No infrastructure reported"))]
        observation = (f'{presence["yes"]:,} of {denominator:,} valid main-season plot responses '
                       f'report irrigation infrastructure ({rate(presence["share"])}).')
        implication = ("This can guide follow-up about recorded infrastructure and its condition. "
                       "Infrastructure presence does not establish actual irrigation use, reliable water "
                       "supply or unmet need; a no response does not prove a plot is rain-fed.")
    else:
        selected = bundle["method" if selection == OPTIONS[1] else "source"]
        denominator, eligible, rows = selected["denominator"], selected["eligible"], selected["categories"]
        if denominator:
            top = max(rows, key=lambda r: r["count"])
            tied = sum(r["count"] == top["count"] for r in rows) > 1
            opening = "One of the largest recorded categories is" if tied else "The largest recorded category is"
            observation = (f'{opening} {top["label"]}: {top["count"]:,} of '
                           f'{denominator:,} valid responses ({rate(top["share"])}).')
        else:
            observation = "No valid eligible responses are available; category percentages are undefined."
        implication = ("Use this distribution to frame follow-up about reported water-management arrangements. "
                       "It describes one main response per eligible plot, not water availability, efficiency "
                       "or investment priority.")
    eligibility = "all main-season roster plots" if selection == OPTIONS[0] else "infrastructure-yes plots only"
    st.caption(f'Percentage denominator: {denominator:,} valid responses from {eligible:,} eligible '
               f'plot records ({eligibility}). Source: NBS NASS 2023; April–October 2022. '
               "Unweighted observed sample, not a national estimate.")
    left, right = st.columns([1.4, 1], gap="large")
    with left:
        st.html(bars(rows, denominator, unit))
    with right:
        st.metric("Eligible plot records", f"{eligible:,}")
        st.metric("Valid response denominator", f"{denominator:,}")
        st.write(observation)
        st.write(implication)
    st.caption(f'{selected["missing"]:,} missing and {selected["invalid"]:,} invalid responses '
               "excluded from this percentage denominator.")
    if selection != OPTIONS[0]:
        st.caption(f'Only the {presence["yes"]:,} infrastructure-yes plots are eligible for this question. '
                   "Missing fields outside that subset are expected skips, not ordinary incompleteness.")
    st.dataframe(pd.DataFrame([{"Response": r["label"], "Plots": r["count"], "Share": rate(r["share"])}
                               for r in rows]), hide_index=True, width="stretch")
    st.caption("Source: NBS NASS 2023; main season April–October 2022. Unweighted observed plot records, "
               "including cultivated plots, temporarily fallow conventional plots and kitchen gardens. "
               "These are plots, not unique households or farmers; no national estimate or confidence interval.")
