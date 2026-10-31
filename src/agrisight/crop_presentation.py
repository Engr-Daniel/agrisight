"""Household crop portfolio and recorded-category diversity, without output claims."""

import pandas as pd
import streamlit as st

from agrisight import reporting_brand as brand
from agrisight.data_context import show as data_context
from agrisight.water_management import bars, rate


def show(bundle: dict) -> None:
    st.subheader("Crop portfolio and diversity")
    st.write("Explore the temporary crops households reported growing and their crop diversity.")
    if bundle["status"] != "available":
        st.info("Reviewed crop portfolio evidence is unavailable. Other agricultural findings remain available.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative crop records, not survey findings.")
    selection = st.selectbox("Explore crop records", ("Crop portfolio", "Recorded diversity"), key="crop_view")
    unit = st.radio("Show crop values as", ("Percentages", "Household counts"), horizontal=True, key="crop_unit")
    c = bundle["counts"]
    n = c["represented_households"]
    data_context("April–October 2022", f"{n:,} households with recorded temporary crops")
    if selection == "Crop portfolio":
        ordered = sorted(bundle["portfolio"], key=lambda r: (-r["households"], r["code"]))
        rows = [{"label": r["label"], "count": r["households"], "share": r["share"]} for r in ordered]
        st.write(f'The chart shows up to ten of the {len(rows):,} observed temporary crop categories; the table contains all categories.')
        shown = rows[:10]
        st.caption("Households may report more than one crop. Each household counts once per crop.")
    else:
        rows = [{"label": r["categories"] + (" recorded category" if r["categories"] == "1" else " recorded categories"),
                 "count": r["households"], "share": r["share"]}
                for r in bundle["diversity"]]
        shown = rows
        mean = bundle["mean_categories"]
        st.metric("Mean recorded temporary crop categories", "Undefined" if mean is None else f"{mean:.2f}")
        st.caption("Each household appears in one diversity group, based on its recorded crop categories.")
    if shown:
        st.html(bars(shown, n, unit, "agri-crop-chart", "represented households"))
    else:
        st.info("No eligible temporary crop records; the portfolio and its percentages are undefined.")
    with st.expander("Read the complete crop table"):
        brand.table(pd.DataFrame([{"Category": r["label"], "Households": r["count"], "Share": rate(r["share"])}
                                   for r in rows]), hide_index=True, width="stretch")
    with st.expander("Understanding these figures — crop portfolio"):
        st.caption(f'{c["temporary_rows"]:,} temporary crop records become {c["household_crop_pairs"]:,} unique household–crop pairs. '
               f'{c["excluded_permanent_rows"]:,} permanent/continuous records are outside this analysis, '
               f'including {c["unlabelled_permanent_rows"]:,} with unlabelled crop codes. No permanent-crop season is inferred.')
        st.write("These findings cover households with recorded temporary crops. See Data Quality for differences from household activity reporting.")
        st.write("Recorded crop frequency does not measure harvest volume, profitability or seed demand. Yam variants remain separate reporting categories; unspecified 'other' crops cannot be identified further.")
