"""Household crop portfolio and recorded-category diversity, without output claims."""

import pandas as pd
import streamlit as st

from agrisight.water_management import bars, rate


def show(bundle: dict) -> None:
    st.subheader("Crop portfolio and diversity")
    st.write("Which temporary crop categories are recorded, and how many does each represented household report?")
    if bundle["status"] != "available":
        st.info("Reviewed crop portfolio evidence is unavailable. Other agricultural findings remain available.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative crop records, not survey findings.")
    selection = st.selectbox("Explore crop records", ("Crop portfolio", "Recorded diversity"), key="crop_view")
    unit = st.radio("Show crop values as", ("Percentages", "Household counts"), horizontal=True, key="crop_unit")
    c = bundle["counts"]
    n = c["represented_households"]
    st.caption(f'Denominator: {n:,} households with at least one recorded temporary crop. '
               "NBS NASS 2023 main-season crop roster, April–October 2022 context; unweighted sample, not national prevalence.")
    if selection == "Crop portfolio":
        ordered = sorted(bundle["portfolio"], key=lambda r: (-r["households"], r["code"]))
        rows = [{"label": r["label"], "count": r["households"], "share": r["share"]} for r in ordered]
        st.write(f'The chart shows up to ten of the {len(rows):,} observed temporary crop categories; the table contains all categories.')
        shown = rows[:10]
        st.write("Each household counts once per crop across all its plots. Crop shares overlap and must not be added as unique households. This is recording frequency, not a production ranking.")
    else:
        rows = [{"label": r["categories"] + (" recorded category" if r["categories"] == "1" else " recorded categories"),
                 "count": r["households"], "share": r["share"]}
                for r in bundle["diversity"]]
        shown = rows
        mean = bundle["mean_categories"]
        st.metric("Mean recorded temporary crop categories", "Undefined" if mean is None else f"{mean:.2f}")
        st.write("Diversity bins count households once and sum to the represented-household denominator. Crop categories are released reporting categories, not botanical species or a measure of resilience.")
    if shown:
        st.html(bars(shown, n, unit, "agri-crop-chart", "represented households"))
    else:
        st.info("No eligible temporary crop records; the portfolio and its percentages are undefined.")
    with st.expander("Read the complete crop table"):
        st.dataframe(pd.DataFrame([{"Category": r["label"], "Households": r["count"], "Share": rate(r["share"])}
                                   for r in rows]), hide_index=True, width="stretch")
    st.caption(f'{c["temporary_rows"]:,} temporary crop records become {c["household_crop_pairs"]:,} unique household–crop pairs. '
               f'{c["excluded_permanent_rows"]:,} permanent/continuous records are outside this analysis, '
               f'including {c["unlabelled_permanent_rows"]:,} with unlabelled crop codes. No permanent-crop season is inferred.')
    missing = c["crop_yes_households_without_temporary_record"]
    inconsistent = c["temporary_households_without_crop_yes"]
    st.caption(f'{missing:,} main-season crop-yes households have no eligible temporary record; '
               f'{inconsistent:,} represented households lack a crop-yes response. These universes are checked, not assumed equal.')
    if missing or inconsistent:
        st.warning("Crop-roster coverage differs from the household participation question. Interpret these results only for represented temporary-crop households; investigate the coverage differences before broader comparisons.")
    st.write("Use this portfolio to frame crop-specific follow-up questions. It does not establish harvest volume, profitability, seed demand or national crop prevalence. Variants such as yam categories remain separate; unspecified 'other' categories do not identify individual crops.")
