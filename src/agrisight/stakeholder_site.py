"""Agricultural intelligence website; reads aggregate evidence only."""

from pathlib import Path

import pandas as pd
import streamlit as st

from agrisight import (
    activity_explorer,
    conditions_presentation,
    conditions_reporting,
    coverage_map,
    coverage_reporting,
    crop_presentation,
    crop_reporting,
    irrigation_reporting,
    seed_presentation,
    seed_reporting,
    stakeholder_reporting,
    water_management,
    website,
)
from agrisight import reporting_brand as brand
from agrisight import reporting_visuals as visuals

PAGES = ("Overview", "Agricultural insights", "Data quality", "Recommendations", "About AgriSight")
SCOPE = ("NBS NASS 2023 · Figures count surveyed households and plots without survey weights; "
         "these are not national estimates.")
# subject: (topic, scene, icon, question, lead). One level of navigation; the topic is a label.
SUBJECTS = {
    "Activities": ("Activities", "livestock", ":material/agriculture:", "What do households farm?",
                   ("Compare the crop, livestock and fish activities households reported, and where "
                   "crop and livestock reports overlap.")),
    "Crop portfolio": ("Crops & seeds", "crops", ":material/grass:", "Which crops do households grow?",
                       "The temporary crops households recorded, and how many different crops each grows."),
    "Seed sources": ("Crops & seeds", "seeds", ":material/spa:", "Where does seed come from?",
                     "Seed channels reported for each recorded crop, and which channels occur together."),
    "Input records": ("Crops & seeds", "inputs", ":material/compost:", "Which farm inputs are recorded?",
                      "Fertiliser, manure and crop-protection records, and where quantities are missing."),
    "Water management": ("Water & land", "irrigation", ":material/water_drop:", "How are plots watered?",
                         "Reported irrigation infrastructure, methods and water sources on main-season plots."),
    "Land & travel": ("Water & land", "land", ":material/landscape:", "How is land held and reached?",
                      "Tenure arrangements, travel time to plots and how households get there."),
    "Plot types": ("Water & land", "garden", ":material/grid_view:", "What kinds of plots are recorded?",
                   "Cultivated plots, temporarily fallow plots and kitchen gardens."),
    "Harvest difficulties": ("Harvest & markets", "harvest", ":material/thunderstorm:",
                             "What disrupts the harvest?",
                             ("Whether crops were harvested, the reasons given when they were not, and "
                             "reported weather and pest shocks.")),
    "Sales & storage": ("Harvest & markets", "market", ":material/storefront:", "What happens after harvest?",
                        "Crop sales, storage and broad loss reports, overall and by crop."),
}
TOPICS = (
    ("Activities", "fish_capture", "Crops, livestock, fish farming and fish capture, side by side."),
    ("Crops & seeds", "crops", "The crops grown, where seed comes from and which inputs are recorded."),
    ("Water & land", "irrigation", "Irrigation, land tenure, travel to plots and the kinds of plots farmed."),
    ("Harvest & markets", "market", "Harvest difficulties, crop sales, storage and reported losses."),
)
READING = (
    ("Start with the question", "Each view answers one plain question about farming households."),
    ("Check who is counted", "Households, plots or crop records: the counting unit changes the meaning."),
    ("Note the period", "Main-season crops cover April–October 2022; other activities the 2022/2023 year."),
    ("Read the limits", "Survey answers describe the sample; they do not measure output, income or impact."),
)


def go(page: str) -> None:
    st.session_state["product_page"] = page


def open_subject(subject: str) -> None:
    st.session_state["subject"] = st.session_state["subject_last"] = subject
    st.session_state["product_page"] = "Agricultural insights"


def keep_subject() -> None:
    """Pills can be deselected; keep the last subject instead of showing nothing."""
    if st.session_state.get("subject") is None:
        st.session_state["subject"] = st.session_state.get("subject_last", "Activities")


def rate(value: float | None) -> str:
    return "Undefined" if value is None else f"{100 * value:.2f}%"


def scope() -> None:
    st.markdown(f'<div class="agri-scope"><b>Source</b> {SCOPE}</div>', unsafe_allow_html=True)


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
        st.write("Compare all activities, or select one to explore its reported participation.")
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
                         f'{item["label"].lower()} during {item["period"]}.')
            brand.table(pd.DataFrame({"Response": ["Yes", "No", "Missing", "Invalid"],
                "Households": [item[k] for k in ("yes", "no", "missing", "invalid")]}),
                hide_index=True, width="stretch")
        st.caption(f'Period: {item["period"]}. Percentage = yes / (yes + no). '
                   f'{item["input_rows"]:,} input household records; '
                   f'{item["missing"]:,} missing and {item["invalid"]:,} invalid responses excluded.')
    brand.table(pd.DataFrame([{
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
    st.caption("Households may report multiple activities. Reporting periods differ by activity.")
    with st.expander("Understanding these figures — activities"):
        st.write("Crops: April–October 2022. Livestock and fish: 2022/2023 agricultural year. "
                 "Activity counts overlap; adding them does not give distinct households. "
                 "These are not same-season measurements. Participation does not measure production, income or service need.")


def insights(bundle: dict, root: Path) -> None:
    # Widget state is dropped while another page is shown; restore the last subject.
    st.session_state.setdefault("subject", st.session_state.get("subject_last", "Activities"))
    keep_subject()
    subject = st.session_state["subject"]
    topic, scene, _, question, lead = SUBJECTS[subject]
    st.html(website.banner(f"Agricultural insights · {topic}", question, lead, scene, compact=True))
    with st.container(key="subject_nav"):
        st.pills("Choose a subject", list(SUBJECTS), key="subject", on_change=keep_subject,
                 format_func=lambda name: f"{SUBJECTS[name][2]} {name}")
    st.session_state["subject_last"] = subject
    scope()
    households, plots = bundle["activities"][0]["input_rows"], bundle["plots"]["total"]
    crop_yes = bundle["activities"][0]["yes"]
    if subject == "Activities":
        activity_story(bundle)
        with st.expander("Crop and livestock overlap"):
            activity_overlap(bundle)
        with st.expander("Where the survey sample is represented"), st.container(key="coverage_map"):
            coverage_map.show(coverage_reporting.build_bundle(root, households))
    elif subject == "Crop portfolio":
        with st.container(key="crop_portfolio"):
            crop_presentation.show(crop_reporting.build_bundle(root, households, plots, crop_yes))
    elif subject == "Seed sources":
        with st.container(key="seed_sources"):
            seed_presentation.show(seed_reporting.build_bundle(root, households, crop_yes))
    elif subject == "Water management":
        with st.container(key="water_management"):
            water_management.show(irrigation_reporting.build_bundle(root, plots))
    elif subject == "Plot types":
        plot_types(bundle)
    else:
        key, name = {"Input records": ("input_records", "inputs"),
                     "Land & travel": ("land_travel", "land"),
                     "Harvest difficulties": ("harvest_difficulties", "harvest"),
                     "Sales & storage": ("crop_destinations", "markets")}[subject]
        fc = conditions_reporting.build_bundle(root, households, plots, bundle["origin"])
        with st.container(key=key):
            conditions_presentation.show_topic(fc, name)


def activity_overlap(bundle: dict) -> None:
    st.subheader("Where crop and livestock reports overlap")
    overlap = bundle["overlap"]
    st.html(website.overlap_mosaic(overlap))
    brand.table(pd.DataFrame([{
        "Main-season crops": c["crops"].capitalize(),
        "Annual livestock / poultry": c["livestock"].capitalize(),
        "Households": c["count"],
    } for c in overlap["cells"]]), hide_index=True, width="stretch")
    st.caption(f'{overlap["denominator"]:,} households with valid responses to both questions; '
               f'{overlap["excluded"]:,} excluded. Crops: April–October 2022; livestock: '
               "2022/2023 agricultural year. Co-reporting does not establish simultaneous "
               "activity, integration or a causal relationship.")


def plot_types(bundle: dict) -> None:
    st.subheader("What kinds of plots were recorded?")
    frame = pd.DataFrame(bundle["plot_types"])
    chart = frame.assign(label=["Cultivated", "Fallow", "Garden"])
    st.bar_chart(chart.rename(columns={"label": "Plot type", "count": "Plots"}),
                 x="Plot type", y="Plots", horizontal=True, height=220, color="#427650")
    brand.table(frame.rename(columns={"label": "Plot type", "count": "Plots"})
                [["Plot type", "Plots"]], hide_index=True, width="stretch")
    st.caption(f'Denominator: all {bundle["plots"]["total"]:,} main-season roster plots, '
               "including temporarily fallow plots and kitchen gardens. Counts are plots, "
               "not people, households or cultivated acreage. Period: April–October 2022.")


def quality(bundle: dict, root: Path) -> None:
    st.html(website.banner("Data quality", "Know what the data can carry",
                           "Check what was recorded, what is missing and which comparisons are held "
                           "back before deciding how to use a finding.", "survey"))
    scope()
    crop = crop_reporting.build_bundle(root, bundle["activities"][0]["input_rows"],
                                       bundle["plots"]["total"], bundle["activities"][0]["yes"])
    st.subheader("Crop portfolio coverage")
    if crop["status"] == "available":
        c = crop["counts"]
        st.write(f'{c["represented_households"]:,} households have recorded temporary crops. '
                 f'{c["crop_yes_households_without_temporary_record"]:,} households report crop activity without an eligible temporary-crop record.')
        with st.expander("Understanding the crop coverage difference"):
            st.write("The household activity question and the temporary-crop portfolio cover different groups. "
                     "A missing temporary-crop record does not automatically mean missing agricultural activity or a permanent-crop-only household.")
            st.caption(f'{c["temporary_households_without_crop_yes"]:,} portfolio households lack a crop-yes response. '
                       f'{c["excluded_permanent_rows"]:,} permanent crop records are outside the portfolio.')
    else:
        st.info("Reviewed crop portfolio evidence is unavailable; coverage details are hidden.")
    fc = conditions_reporting.build_bundle(root, bundle["activities"][0]["input_rows"],
                                           bundle["plots"]["total"], bundle["origin"])
    st.subheader("Input quantity completeness")
    if fc["status"] == "available":
        st.caption("Recorded household–input rows; missing quantity is not zero use.")
        brand.table(pd.DataFrame([{"Input": r["label"], "Recorded rows": r["records"],
            "Missing quantity": r["statuses"][2]["count"],
            "Missing share": rate(r["statuses"][2]["share"])} for r in fc["inputs"]]), hide_index=True, width="stretch")
    else:
        st.info("Reviewed input-record evidence is unavailable; completeness details are hidden.")
    st.subheader("Activity response completeness")
    brand.table(pd.DataFrame([{
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
    st.html(website.banner("Recommendations", "From findings to next questions",
                           "Practical follow-up suggested by the findings. They frame questions and "
                           "checks; they do not establish programme impact, targeting priorities or "
                           "a budget allocation.", "land"))
    scope()
    crops = bundle["activities"][0]
    both = bundle["overlap"]["cells"][0]["count"]
    plots = bundle["plots"]
    items = (
        ("Investigate households reporting crops and livestock",
         (f'{both:,} of {bundle["overlap"]["denominator"]:,} households that answered both questions '
         "report both activities. Investigate whether services need to account for multiple "
         "activities; confirm timing and actual service needs before designing an intervention."),
         ("Evidence: Agricultural insights → Activities → overlap. Main-season crops (April–October 2022) "
         "and annual livestock (2022/2023); co-reporting is not evidence of integrated farming.")),
        ("Check the needs behind reported activities",
         (f'Main-season crops were reported by {crops["yes"]:,} of {crops["denominator"]:,} households '
         f'with a valid answer ({rate(crops["share"])}). Use the activity figures to frame follow-up '
         "questions; do not infer production volumes, profitability or population demand from "
         "participation alone."),
         ("Evidence: Agricultural insights → Activities. Crop period: April–October 2022. Other activity "
         "periods differ; surveyed sample only.")),
        ("Confirm how plot areas were measured before planning acreage",
         ("The released plot-area field is labelled square metres, but how the areas were measured is "
         "not documented. Confirm measurement provenance and survey design before using area summaries "
         f'for operational planning or national inference. Separately, {plots["missing_area"]:,} of '
         f'{plots["total"]:,} plot-area values are missing.'),
         "Evidence: Data quality → plot-area coverage, main season April–October 2022."),
    )
    for number, (title, body, evidence) in enumerate(items, 1):
        with st.container(key=f"rec_{number}"):
            st.markdown(f'<span class="agri-rec-no">RECOMMENDATION {number:02d}</span>',
                        unsafe_allow_html=True)
            st.subheader(title)
            st.write(body)
            st.caption(evidence)
    with st.container(horizontal=True):
        st.button("Explore the evidence", type="primary", on_click=go, args=("Agricultural insights",))
        st.button("Check coverage and limitations", on_click=go, args=("Data quality",))


def about() -> None:
    st.html(website.banner("About AgriSight", "Agricultural evidence, clearly told",
                           "AgriSight turns agricultural survey data into understandable evidence for "
                           "decision support: what households reported, where activities overlap and "
                           "where data quality limits a conclusion.", "fish_capture"))
    st.subheader("Source and scope")
    st.write(SCOPE)
    st.write("The current findings describe main-season crops and plots in April–October 2022 "
             "and livestock and fish activities in the 2022/2023 agricultural year. Historical "
             "survey responses do not describe current conditions.")
    st.write("Explore reported agricultural activities and farming conditions to frame practical follow-up questions.")
    with st.expander("What these figures can and cannot tell you"):
        st.write("Participation does not measure output, income or programme impact. National inference "
                 "and minor-season comparisons require further source and methods review. "
                 "The state map describes sample coverage, not geographic agricultural prevalence.")
    st.markdown("[NBS source catalogue](https://microdata.nigerianstat.gov.ng/index.php/catalog/173)")
    st.html(website.heading("Reading the evidence", "How to read a finding"))
    st.html(website.steps(READING))


def key_figures(bundle: dict, root: Path) -> list[tuple[str, str, str]]:
    """Headline counts; optional evidence that cannot be verified is left out, never filled in."""
    households, plots = bundle["activities"][0]["input_rows"], bundle["plots"]["total"]
    items = [(f"{households:,}", "Households surveyed", "Released household records"),
             (f"{plots:,}", "Farm plots recorded", "Main season, April–October 2022")]
    crop = crop_reporting.build_bundle(root, households, plots, bundle["activities"][0]["yes"])
    if crop["status"] == "available":
        items.append((f'{len(crop["portfolio"]):,}', "Temporary crop types",
                      "Recorded in household crop lists"))
    coverage = coverage_reporting.build_bundle(root, households)
    if coverage["status"] == "available" and not coverage["suppressed"]:
        areas = sum(1 for s in coverage["states"] if s["households"])
        items.append((f"{areas:,}", "States and FCT represented", "Areas with sampled households"))
    return items


def overview(bundle: dict, root: Path) -> None:
    activities = sorted(bundle["activities"], key=lambda a: activity_explorer.ORDER.index(a["id"]))
    st.html(website.figures(key_figures(bundle, root)))
    st.html(website.heading("What households do", "Most households grow crops; many also keep livestock",
                            "The share of surveyed households reporting each activity. Households "
                            "can report several activities, so the shares do not add up to 100%."))
    st.html(website.activity_cards(activities))
    st.caption("Main-season crops: April–October 2022. Livestock and fish: 2022/2023 agricultural year. "
               "Participation does not measure production, income or service need.")
    overlap = bundle["overlap"]
    both = overlap["cells"][0]["count"]
    share = both / overlap["denominator"] if overlap["denominator"] else None
    st.html(website.heading("Crops and livestock together",
                            f"{website.pct(share, 0)} reported both crops and livestock",
                            "How the two answers combine for each household that answered both questions."))
    st.html(website.overlap_mosaic(overlap))
    st.caption(f'{overlap["excluded"]:,} households without a valid answer to both questions are '
               "excluded. Crops cover April–October 2022 and livestock the 2022/2023 year, so "
               "co-reporting does not show the activities happened at the same time or were integrated.")
    st.html(website.heading("Explore by topic", "Nine questions, four topics",
                            "Open any subject to see its chart, the counts behind it and how to read it."))
    columns = st.columns(4, gap="medium")
    for index, (column, (topic, scene, lead)) in enumerate(zip(columns, TOPICS, strict=True)):
        with column, st.container(key=f"topic_{index}"):
            st.html(website.topic_card(scene, topic, lead))
            with st.container(horizontal=True, gap="small"):
                for subject, (group, *_) in SUBJECTS.items():
                    if group == topic:
                        st.button(subject, key=f"open_{subject}", on_click=open_subject,
                                  args=(subject,))
    st.html(website.heading("Reading the evidence", "How to read a finding"))
    st.html(website.steps(READING))


def run(root: Path) -> None:
    st.set_page_config(page_title="AgriSight | Agricultural intelligence", layout="wide",
                       initial_sidebar_state="collapsed")
    brand.styles()
    brand.website_styles()
    page = st.session_state.get("product_page", "Overview")
    if page not in PAGES:
        page = "Overview"
    brand.navigation(PAGES, page, go)
    if page == "About AgriSight":
        about()
    else:
        bundle = stakeholder_reporting.build_bundle(root)
        available = bundle["status"] == "available"
        if page == "Overview":
            st.html(website.hero(bundle["activities"][0]["input_rows"] if available else None))
            with st.container(horizontal=True, key="hero_cta"):
                st.button("Explore agricultural insights", type="primary", on_click=go,
                          args=("Agricultural insights",))
                st.button("Check data quality", on_click=go, args=("Data quality",))
        if not available:
            scope()
            st.warning("Reviewed survey evidence is unavailable. Findings are hidden until "
                       "the approved aggregate files can be verified.")
        else:
            if bundle["origin"] == "TEST FIXTURE":
                st.warning("TEST FIXTURE — illustrative test records, not survey findings.")
            if page == "Overview":
                scope()
                overview(bundle, root)
            elif page == "Agricultural insights":
                insights(bundle, root)
            elif page == "Data quality":
                quality(bundle, root)
            elif page == "Recommendations":
                recommendations(bundle)
    st.html(website.footer(SCOPE))
