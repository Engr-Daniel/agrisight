"""Agricultural intelligence website; reads aggregate evidence only."""

from pathlib import Path

import pandas as pd
import streamlit as st

from agrisight import reporting_brand as brand
from agrisight import reporting_visuals as visuals
from agrisight import stakeholder_reporting

PAGES = ("Overview", "Agricultural insights", "Data quality", "Recommendations", "About AgriSight")
SCOPE = ("NBS National Agricultural Sample Survey (NASS) 2023. Unweighted observed sample; "
         "these are not national estimates. Households and plots are different counting units.")


def go(page: str) -> None:
    st.session_state["product_page"] = page


def rate(value: float | None) -> str:
    return "Undefined" if value is None else f"{100 * value:.2f}%"


def activity_story(bundle: dict) -> None:
    activities = bundle["activities"]
    index = st.selectbox("Explore an agricultural activity", range(4),
                         format_func=lambda i: activities[i]["label"], key="activity")
    item = activities[index]
    columns = st.columns(3)
    columns[0].metric("Households reporting activity", f'{item["yes"]:,}')
    columns[1].metric("Share of valid responses", rate(item["share"]))
    columns[2].metric("Valid household responses", f'{item["denominator"]:,}')
    st.caption(f'Period: {item["period"]}. Yes / (yes + no); '
               f'{item["missing"]:,} missing and {item["invalid"]:,} invalid responses excluded.')
    st.html(visuals.waffle(item["share"], "Reported activity", "Did not report activity"))
    st.dataframe(pd.DataFrame([{
        "Activity": a["label"], "Reference period": a["period"],
        "Households: yes": a["yes"], "Valid responses": a["denominator"],
        "Share": rate(a["share"]),
    } for a in activities]), hide_index=True, width="stretch")
    st.caption("Households may report several activities. Do not add activity counts to count "
               "distinct households. Crop and annual activity questions cover different periods.")


def insights(bundle: dict) -> None:
    st.title("Agricultural insights")
    st.write("Understand the activities reported by households and the plots in the survey roster.")
    activity_story(bundle)
    st.subheader("Where crop and livestock reports overlap")
    overlap = bundle["overlap"]
    st.dataframe(pd.DataFrame([{
        "Main-season crops": c["crops"], "Annual livestock / poultry": c["livestock"],
        "Households": c["count"],
    } for c in overlap["cells"]]), hide_index=True, width="stretch")
    st.caption(f'{overlap["denominator"]:,} households with valid responses to both questions; '
               f'{overlap["excluded"]:,} excluded. Crops: April–October 2022; livestock: '
               "2022/2023 agricultural year. Co-reporting does not establish simultaneous "
               "activity, integration or a causal relationship.")
    st.subheader("What kinds of plots were recorded?")
    frame = pd.DataFrame(bundle["plot_types"])
    chart = frame.assign(label=["Cultivated", "Fallow", "Garden"])
    st.bar_chart(chart.rename(columns={"label": "Plot type", "count": "Plots"}),
                 x="Plot type", y="Plots", horizontal=True, height=220, color="#427650")
    st.dataframe(frame.rename(columns={"label": "Plot type", "count": "Plots"})
                 [["Plot type", "Plots"]], hide_index=True, width="stretch")
    st.caption(f'Denominator: all {bundle["plots"]["total"]:,} main-season roster plots, '
               "including temporarily fallow plots and kitchen gardens. Counts are plots, "
               "not people, households or cultivated acreage. Period: April–October 2022.")


def quality(bundle: dict) -> None:
    st.title("Data quality")
    st.write("Check what is recorded before deciding how to use a finding.")
    st.subheader("Activity response completeness")
    st.dataframe(pd.DataFrame([{
        "Activity": a["label"], "Household records": a["input_rows"],
        "Valid responses": a["denominator"], "Missing": a["missing"], "Invalid": a["invalid"],
    } for a in bundle["activities"]]), hide_index=True, width="stretch")
    st.caption("Valid means a released yes/no response. Completeness does not establish accuracy "
               "or representativeness. Crop period: April–October 2022; other activities: "
               "2022/2023 agricultural year.")
    plots = bundle["plots"]
    st.subheader("Plot-area coverage")
    left, right = st.columns(2)
    left.metric("Recorded area values", f'{plots["recorded_area"]:,}')
    right.metric("Missing area values", f'{plots["missing_area"]:,}')
    st.caption(f'Denominator: {plots["total"]:,} main-season roster plots (April–October 2022). '
               "Missing values remain missing; no companion-field backfill was used.")
    st.warning("The released area field is labelled square metres, but its measurement lineage "
               "is unresolved. It cannot certify physical acreage. Usable survey variance design "
               "has not been established, so national estimates and confidence intervals are excluded.")
    st.info("Minor-season comparisons remain excluded because the reference calendar conflicts. "
            "Geographic analysis awaits boundary, identifier and disclosure review.")


def recommendations(bundle: dict) -> None:
    st.title("Recommendations")
    st.write("Use these findings to guide further questions and data checks. They do not establish "
             "programme impact, targeting priorities or a budget allocation.")
    crops = bundle["activities"][0]
    both = bundle["overlap"]["cells"][0]["count"]
    st.subheader("Investigate households reporting crops and livestock")
    st.write(f'{both:,} of {bundle["overlap"]["denominator"]:,} jointly valid households report '
             "both activities. Investigate whether services need to account for multiple activities; "
             "confirm timing and actual service needs before designing an intervention.")
    st.caption("Evidence: Agricultural insights → overlap. Main-season crops (April–October 2022) "
               "and annual livestock (2022/2023); co-reporting is not evidence of integrated farming.")
    st.subheader("Check the needs behind reported activities")
    st.write(f'Main-season crops were reported by {crops["yes"]:,} of '
             f'{crops["denominator"]:,} valid household responses ({rate(crops["share"])}). '
             "Use the activity table to frame follow-up questions; do not infer production volumes, "
             "profitability or population demand from participation alone.")
    st.caption("Evidence: Agricultural insights → activity table. Crop period: April–October 2022. "
               "Other activity periods differ; unweighted observed sample only.")
    st.subheader("Resolve measurement and coverage before planning acreage")
    st.write(f'{bundle["plots"]["missing_area"]:,} of {bundle["plots"]["total"]:,} plot-area '
             "values are missing. Confirm field measurement provenance and survey design before "
             "using area summaries for operational planning or national inference.")
    st.caption("Evidence: Data quality → plot-area coverage, main season April–October 2022.")
    st.button("Explore the evidence", on_click=go, args=("Agricultural insights",))
    st.button("Check coverage and limitations", on_click=go, args=("Data quality",))


def about() -> None:
    st.title("About AgriSight")
    st.write("AgriSight turns agricultural data into understandable evidence for decision support. "
             "It helps readers ask what households reported, where activities overlap and where "
             "data quality limits a conclusion.")
    st.subheader("Source and scope")
    st.write(SCOPE)
    st.write("The current findings describe main-season crops and plots in April–October 2022 "
             "and livestock and fish activities in the 2022/2023 agricultural year. Historical "
             "survey responses do not describe current conditions.")
    st.write("Participation does not measure output, income or programme impact. No client "
             "engagement, field enrolment or intervention outcome is claimed. National inference, "
             "maps and minor-season comparisons require further source and methods review.")
    st.markdown("[NBS source catalogue](https://microdata.nigerianstat.gov.ng/index.php/catalog/173)")


def run(root: Path) -> None:
    st.set_page_config(page_title="AgriSight | Agricultural intelligence", layout="wide",
                       initial_sidebar_state="collapsed")
    brand.styles()
    page = st.session_state.get("product_page", "Overview")
    if page not in PAGES:
        page = "Overview"
    brand.navigation(PAGES, page, go)
    if page == "About AgriSight":
        about()
    else:
        bundle = stakeholder_reporting.build_bundle(root)
        if page == "Overview":
            brand.hero("AGRICULTURAL DATA INTELLIGENCE & DECISION SUPPORT")
            with st.container(horizontal=True):
                st.button("Explore agricultural insights", type="primary", on_click=go,
                          args=("Agricultural insights",))
                st.button("Check data quality", on_click=go, args=("Data quality",))
        st.caption(SCOPE)
        if bundle["status"] != "available":
            st.warning("Reviewed survey evidence is unavailable. Findings are hidden until "
                       "the approved aggregate files can be verified.")
        else:
            if bundle["origin"] == "TEST FIXTURE":
                st.warning("TEST FIXTURE — illustrative test records, not survey findings.")
            if page == "Overview":
                st.subheader("Understand agricultural activity in the observed sample")
                st.write("Explore household activities, crop–livestock co-reporting and plot types. "
                         "Check coverage and measurement limitations before acting on a finding.")
                activity_story(bundle)
            elif page == "Agricultural insights":
                insights(bundle)
            elif page == "Data quality":
                quality(bundle)
            elif page == "Recommendations":
                recommendations(bundle)
    st.divider()
    st.caption("AgriSight · Agricultural intelligence and decision support. "
               "Historical survey evidence; unweighted observed sample.")
    st.caption(brand.IMAGE_CREDIT)
