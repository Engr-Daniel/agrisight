"""Agricultural intelligence website; reads aggregate evidence only."""

from pathlib import Path

import pandas as pd
import streamlit as st

from agrisight import (
    activity_explorer,
    coverage_map,
    coverage_reporting,
    irrigation_reporting,
    stakeholder_reporting,
    water_management,
)
from agrisight import reporting_brand as brand
from agrisight import reporting_visuals as visuals

PAGES = ("Overview", "Agricultural insights", "Data quality", "Recommendations", "About AgriSight")
SCOPE = ("NBS National Agricultural Sample Survey (NASS) 2023. Unweighted observed sample; "
         "these are not national estimates. Households and plots are different counting units.")


def go(page: str) -> None:
    st.session_state["product_page"] = page


def rate(value: float | None) -> str:
    return "Undefined" if value is None else f"{100 * value:.2f}%"


def activity_story(bundle: dict) -> None:
    st.subheader("Agricultural activity explorer")
    activities = bundle["activities"]
    by_id = {a["id"]: a for a in activities}
    selected = st.selectbox("Explore agricultural activities", ("all", *activity_explorer.ORDER),
                            format_func=lambda key: "All activities" if key == "all" else by_id[key]["label"],
                            key="activity")
    unit = st.radio("Show activity values as", ("Percentages", "Household counts"),
                    horizontal=True, key="activity_unit")
    if selected == "all":
        st.html(activity_explorer.chart(activities, unit))
        st.write("Read the complete activity picture, then select an activity to examine its "
                 "responses and interpretation. Participation measures reporting, not output or income.")
    else:
        item = by_id[selected]
        visual, explanation = st.columns([1.3, 1], gap="large")
        with visual:
            st.html(activity_explorer.chart([item], unit))
            st.html(visuals.waffle(item["share"], "Reported activity", "Did not report activity"))
        with explanation:
            st.metric("Share of valid responses", rate(item["share"]))
            st.metric("Households reporting activity", f'{item["yes"]:,}')
            st.metric("Valid household responses", f'{item["denominator"]:,}')
            if item["share"] is None:
                st.write("No valid yes/no responses are available; the percentage is undefined.")
            else:
                st.write(f'{rate(item["share"])} of valid household responses reported '
                         f'{item["label"].lower()} during {item["period"]}. This describes '
                         "the observed sample; it does not measure production, income or service need.")
            st.dataframe(pd.DataFrame({"Response": ["Yes", "No", "Missing", "Invalid"],
                "Households": [item[k] for k in ("yes", "no", "missing", "invalid")]}),
                hide_index=True, width="stretch")
        st.caption(f'Period: {item["period"]}. Percentage = yes / (yes + no). '
                   f'{item["input_rows"]:,} input household records; '
                   f'{item["missing"]:,} missing and {item["invalid"]:,} invalid responses excluded.')
    st.dataframe(pd.DataFrame([{
        "Activity": a["label"], "Reference period": a["period"],
        "Households: yes": a["yes"], "Valid responses": a["denominator"],
        "Share": rate(a["share"]),
    } for a in activities]), hide_index=True, width="stretch")
    denominators = {a["denominator"] for a in activities}
    if len(denominators) == 1:
        st.caption(f'Each activity uses {next(iter(denominators)):,} valid household responses '
                   "as its percentage denominator.")
    else:
        st.caption("Percentage denominators differ by activity; see the valid responses in the table.")
    st.caption("Responses can overlap: do not add activity counts to count distinct households. "
               "Crops: April–October 2022; livestock and fish: 2022/2023 agricultural year. "
               "Visual comparison is not a same-season comparison or a set of mutually exclusive categories.")


def insights(bundle: dict, root: Path) -> None:
    st.title("Agricultural insights")
    st.write("Understand the activities reported by households and the plots in the survey roster.")
    activity_story(bundle)
    with st.container(key="water_management"):
        water_management.show(irrigation_reporting.build_bundle(root, bundle["plots"]["total"]))
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
    with st.container(key="coverage_map"):
        coverage_map.show(coverage_reporting.build_bundle(root, bundle["activities"][0]["input_rows"]))


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
            "The state map describes sample coverage only; geographic population comparisons remain excluded.")


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
             "engagement, field enrolment or intervention outcome is claimed. National inference "
             "and minor-season comparisons require further source and methods review. "
             "The state map describes sample coverage; it does not estimate geographic agricultural prevalence.")
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
                insights(bundle, root)
            elif page == "Data quality":
                quality(bundle)
            elif page == "Recommendations":
                recommendations(bundle)
    st.divider()
    st.caption("AgriSight · Agricultural intelligence and decision support. "
               "Historical survey evidence; unweighted observed sample.")
    st.caption(brand.IMAGE_CREDIT)
