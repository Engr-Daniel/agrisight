"""Offline state polygons; only aggregate sample coverage is encoded."""

import altair as alt
import pandas as pd
import streamlit as st


def show(bundle: dict) -> None:
    st.subheader("Where the household sample is represented")
    st.write("The map shows released household records by state and FCT. Darker green means "
             "more records in this sample, not more farming or greater service need.")
    if bundle["status"] != "available":
        st.info("The coverage map is unavailable because its reviewed inputs could not be verified. "
                "The activity and plot findings remain available.")
        return
    chart = alt.Chart(alt.Data(values=bundle["features"])).mark_geoshape(
        stroke="#fffef9", strokeWidth=0.8)
    if bundle["suppressed"]:
        chart = chart.encode(color=alt.value("#c4d5b2"), tooltip=[alt.Tooltip("properties.name:N", title="State / FCT")])
        st.info("Regional counts are withheld because at least one area has fewer than 30 records. "
                "Uniform colour conveys boundaries only; no numeric tooltips or count table are shown.")
    else:
        chart = chart.encode(color=alt.Color("properties.households:Q",
            title="Sample households", scale=alt.Scale(scheme="greens", zero=True),
            legend=alt.Legend(orient="bottom", direction="horizontal", gradientLength=220)),
            tooltip=[alt.Tooltip("properties.name:N", title="State / FCT"),
                     alt.Tooltip("properties.households:Q", title="Sample households", format=",")])
    st.altair_chart(chart.project(type="mercator").properties(height=410)
                    .configure_view(stroke=None).configure(background="#f6f7f0"), width="stretch")
    if not bundle["suppressed"]:
        with st.expander("Read the state coverage table"):
            st.dataframe(pd.DataFrame(bundle["states"]).rename(columns={
                "name": "State / FCT", "households": "Sample household records"}),
                hide_index=True, width="stretch")
    st.caption("Source: NBS NASS 2023 released household sample; unweighted counts, not population "
               "estimates. Coverage is not agricultural prevalence. No household locations or smaller-area drill-down.")
    st.caption("Reference context: crops April–October 2022; annual activities 2022/2023. "
               "Map counts describe the released records, not activity-specific seasonal participation.")
    st.markdown("Boundaries: GRID3 / [geoBoundaries gbOpen](https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/), "
                "2022 representation, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
                "Simplified administrative boundaries for contextual display, "
                "not cadastral or survey-boundary certification.")
