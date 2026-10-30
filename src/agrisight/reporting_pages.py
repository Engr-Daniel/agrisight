"""Stakeholder website pages over the same validated bundle as the technical explorer."""

import streamlit as st

from agrisight import reporting_brand
from agrisight import reporting_visuals as visuals
from agrisight.reporting_ui import decimal, integer, percentage


def go(page: str, view: str | None = None, indicator: str | None = None) -> None:
    """Callbacks change navigation only; never persist evidence or derived values."""
    st.session_state["page"] = page
    if view is not None:
        st.session_state["view"] = view
    if indicator is not None:
        st.session_state["indicator"] = indicator
    if view == "Synthetic quality":
        st.session_state.update(seed=303, scenario="Mixed", baseline="B1",
                                evaluation="Matching", relation="duplicate_role")
    if view == "Workload measurements":
        st.session_state.update(workload="55000:0", measurement="timing")


def link(label: str, key: str, view: str, indicator: str | None = None) -> None:
    st.button(label, key=key, on_click=go, icon=":material/arrow_forward:",
              icon_position="right", args=("Evidence & methods", view, indicator))


def survey_panel(bundle: dict) -> dict | None:
    panel = bundle["panels"]["survey"]
    if panel["status"] != "available":
        st.warning("Survey findings are unavailable. No summary figures are shown until "
                   "the reviewed evidence is available again.")
        return None
    return panel


def source(panel: dict) -> None:
    st.caption(f"Source: {panel['origin']} | Reference: {panel['reference_period']}")


def stat(column, key: str, art: str, kicker: str, label: str, value: str, meaning: str) -> None:
    with column, st.container(border=True, key=key):
        st.html(visuals.stat_head(art, kicker))
        st.metric(label, value)
        st.caption(meaning)


def participation_story(first: dict) -> None:
    counts, proportion = first["counts"], first["values"]["proportion"]
    if proportion is None:
        st.info("Participation is not defined because there are no valid responses.")
        return
    share = visuals.per_hundred(proportion)
    phrase = f"About {share} in every 100"
    if 0 < proportion < 1 and share == 0:
        phrase = "Fewer than 1 in every 100"
    elif 0 < proportion < 1 and share == 100:
        phrase = "More than 99 in every 100"
    st.markdown(f"### {phrase} households grew crops in the main season")
    st.write(f"{integer(counts['numerator'])} of {integer(counts['denominator'])} households "
             f"that gave a valid answer reported growing crops: {percentage(proportion)}.")


def area_story(second: dict) -> bool:
    """Plain-language plot size; only when the median is a single known value."""
    values = second["values"]
    lower, upper = values["full_roster_lower_m2"], values["full_roster_upper_m2"]
    if second["status"] != "bounded" or lower is None or lower != upper:
        return False
    st.markdown(f"### The recorded median plot area is about {lower/10_000:,.2f} hectares")
    st.write(f"The median is about {decimal(lower, 2)} square metres in the released labelled "
             "units: the midpoint of the ordered area values, not a whole-farm total.")
    return True


def overview(bundle: dict) -> None:
    reporting_brand.hero("Agricultural data intelligence")
    with st.container(horizontal=True, key="agri_hero_actions"):
        st.button("Explore agricultural insights", key="explore_insights", type="primary",
                  on_click=go, args=("Agricultural insights",))
        st.button("Open technical evidence", key="open_evidence", on_click=go,
                  args=("Evidence & methods", "Survey findings"))
    st.html(visuals.section("At a glance", "The survey at a glance",
                            "Three numbers from the released survey sample, each counted "
                            "in its own unit."))
    panel = survey_panel(bundle)
    if panel:
        first, second = panel["records"]
        counts, areas = first["counts"], second["counts"]
        columns = st.columns(3)
        stat(columns[0], "stat_households", "household", "Households", "Household records",
             integer(counts["input_rows"]),
             "Agricultural household records released in the survey sample.")
        stat(columns[1], "stat_plots", "plots", "Farm plots", "Plot records",
             integer(areas["total_plots"]), "Main-season plots listed by those households.")
        stat(columns[2], "stat_participation", "sprout", "Crop growing", "Crop participation",
             percentage(first["values"]["proportion"]),
             "Share of valid household answers reporting main-season crops.")
        st.caption(f"Participation: {integer(counts['numerator'])} yes responses / "
                   f"{integer(counts['denominator'])} valid household responses. "
                   "Households and plots are different units; these counts are not added.")
        source(panel)
        st.info("Historical, unweighted sample findings. Not national estimates or current "
                "field conditions; population uncertainty is not estimated.")
        st.html(visuals.section("The story", "What the households told us"))
        with st.container(border=True, key="story_participation"):
            art, words = st.columns([2, 3], vertical_alignment="center")
            art.html(visuals.waffle(first["values"]["proportion"],
                                    "grew main-season crops", "did not"))
            with words:
                participation_story(first)
                st.button("Read the full finding", key="read_participation", on_click=go,
                          args=("Agricultural insights",), icon=":material/arrow_forward:",
                          icon_position="right")
        with st.container(border=True, key="story_area"):
            art, words = st.columns([2, 3], vertical_alignment="center")
            with words:
                if not area_story(second):
                    st.markdown("### Plot sizes are reported with their gaps in view")
                st.write(f"{integer(areas['missing_areas'])} of {integer(areas['total_plots'])} "
                         "plots have no recorded area, and that is shown, not hidden.")
                st.caption("Released labelled units; measurement lineage is unverified. "
                           "Not a national farm-size estimate.")
            if second["status"] == "bounded" and second["values"]["full_roster_lower_m2"] \
                    == second["values"]["full_roster_upper_m2"]:
                art.html(visuals.plot_square(second["values"]["full_roster_lower_m2"]))
            else:
                art.html(f'<div class="agri-art-icon">{visuals.icon("plots", 120)}</div>')
    st.html(visuals.section("Coverage", "Where the evidence comes from"))
    st.html(visuals.map_pending())
    st.html(visuals.section("Our approach", "How every number is checked",
                            "Each figure follows the same path from official files "
                            "to this page."))
    st.html(visuals.steps([
        ("survey", "Official source", ("Released files from the national agricultural "
         "sample survey, kept unchanged and fingerprinted.")),
        ("check", "Calculated twice", ("Each figure is computed independently in Python and "
         "in SQL. The two must agree exactly.")),
        ("scale", "Limits stated", ("Units, denominators, gaps and what a figure cannot "
         "say are kept beside it.")),
        ("search", "Open to inspection", ("Every finding links to its full evidence, "
         "down to the counts behind it."))]))
    st.html(visuals.section("Explore", "Choose what you want to understand"))
    columns = st.columns(3)
    topics = [("Agricultural insights", "sprout", "What does the released sample show?",
               "Read the crop-participation finding and what is known about plot areas."),
              ("Engineering studies", "shield", "How were analytical methods tested?",
               "See separate synthetic matching and local workload studies."),
              ("Evidence & methods", "search", "What supports each finding?",
               "Inspect definitions, denominators, exclusions and full-precision evidence.")]
    for column, (page, art, title, body) in zip(columns, topics):
        with column, st.container(border=True, key="topic_card_"+art):
            st.html(visuals.icon(art, 48))
            st.markdown(f"#### {title}")
            st.write(body)
            st.button(page, key="topic_"+page, on_click=go, args=(page,),
                      icon=":material/arrow_forward:", icon_position="right")
    st.caption("An independent research and portfolio prototype. Intended audiences are "
               "proposed users; no client deployments or business impact are claimed.")


def insights(bundle: dict) -> None:
    st.html(visuals.banner("Agricultural insights", "What the agricultural sample reveals",
                           "Two findings from the released NASS data, with their scope "
                           "in view.", "sprout"))
    panel = survey_panel(bundle)
    if panel is None:
        return
    source(panel)
    first, second = panel["records"]
    with st.container(border=True, key="finding_participation"):
        st.html(visuals.section("Finding 01", "Main-season crop participation"))
        counts, values = first["counts"], first["values"]
        art, words = st.columns([2, 3], vertical_alignment="center")
        with art:
            st.html(visuals.waffle(values["proportion"], "grew main-season crops", "did not"))
        with words:
            st.metric("Crop participation", percentage(values["proportion"]))
            if values["proportion"] is None:
                st.info("Participation is not defined because there are no valid responses.")
            else:
                st.write(f"{percentage(values['proportion'])} of valid household responses "
                         "reported growing crops in the main season.")
            st.caption(f"{integer(counts['numerator'])} yes / "
                       f"{integer(counts['denominator'])} valid responses; "
                       f"{integer(counts['excluded_count'])} missing/invalid excluded.")
            st.warning("Unweighted released sample, not national or current prevalence. "
                       "No population confidence interval is available.")
            link("Inspect participation evidence", "participation_evidence", "Survey findings",
                 "NASS-01")
    with st.container(border=True, key="finding_area"):
        st.html(visuals.section("Finding 02", "What missing plot areas can change"))
        counts, values = second["counts"], second["values"]
        art, words = st.columns([2, 3], vertical_alignment="center")
        with words:
            st.metric("Missing area values", integer(counts["missing_areas"]))
            if counts["total_plots"]:
                st.progress(counts["observed_areas"]/counts["total_plots"],
                            text=f"{integer(counts['observed_areas'])} / "
                                 f"{integer(counts['total_plots'])} plots have recorded "
                                 "area values")
            if second["status"] == "undefined":
                st.info("The plot roster is empty; its median and bounds are not defined.")
            elif second["status"] == "unbounded":
                st.info("The nonnegative missing-value model gives no finite upper "
                        "median bound.")
            else:
                columns = st.columns(2)
                columns[0].metric("Lower median bound (labelled m²)",
                                  decimal(values["full_roster_lower_m2"], 2))
                columns[1].metric("Upper median bound (labelled m²)",
                                  decimal(values["full_roster_upper_m2"], 2))
                st.write("The bounds show the range of full-roster medians permitted when "
                         "unknown areas may take any nonnegative value.")
                if counts["missing_areas"] and values["width_m2"] == 0:
                    st.write("Here the bounding ranks coincide: the missing entries cannot "
                             "move this median under that model.")
        with art:
            if second["status"] == "bounded" and values["width_m2"] == 0:
                st.html(visuals.plot_square(values["full_roster_lower_m2"]))
            else:
                st.html(f'<div class="agri-art-icon">{visuals.icon("plots", 120)}</div>')
        st.warning("Released labelled units; measurement lineage is unverified. These are "
                   "missing-value bounds, not confidence intervals or a national "
                   "farm-size estimate.")
        link("Inspect area evidence", "area_evidence", "Survey findings", "NASS-02")


def engineering(bundle: dict) -> None:
    st.html(visuals.banner("Engineering studies", "Testing the analytical foundations",
                           "Separate synthetic studies examine matching errors and local "
                           "batch behavior.", "shield"))
    st.write("They do not describe survey respondents or an operational farmer registry.")
    columns = st.columns(2)
    for column, key, title, art in zip(columns, ("synthetic_quality", "synthetic_workload"),
                                       ("Synthetic matching study", "Local workload study"),
                                       ("shield", "timer")):
        panel = bundle["panels"][key]
        with column, st.container(border=True, key="study_"+key):
            st.html(visuals.stat_head(art, "Synthetic data"))
            st.subheader(title)
            st.caption(f"Source: {panel['origin']} | {panel['reference_period']}")
            if panel["status"] != "available":
                st.warning("Study evidence is unavailable; no result is shown.")
                continue
            if key == "synthetic_quality":
                row = next(r for r in panel["records"] if r["selectors"] == {
                    "seed": 303, "configuration": "Mixed", "baseline": "B1",
                    "measure": "duplicate_role"})
                st.caption("Mixed scenario · Seed 303 · B1 · Duplicate role submissions")
                pair = st.columns(2)
                pair[0].metric("Precision", percentage(row["values"]["precision"]))
                pair[1].metric("Recall", percentage(row["values"]["recall"]))
                st.write("False links and missed repeats matter. Inspect both before "
                         "considering how matching rules might be used.")
                st.warning("Synthetic accuracy only. No field accuracy or automatic merging "
                           "claim.")
                link("Inspect matching evidence", "matching_evidence", "Synthetic quality")
            else:
                row = next(r for r in panel["records"] if r["selectors"] == {
                    "events": 55000, "collision": False})
                pair = st.columns(2)
                pair[0].metric("Submission events", integer(row["counts"]["events"]))
                if row["status"] == "success":
                    pair[1].metric("Median batch time (seconds)",
                                   decimal(row["values"]["timing"]["median"], 3))
                else:
                    st.info("This workload has no successful timing result; no time is shown.")
                st.write("Submission events are not distinct people or roles. "
                         "This study measures a specific bounded-key local batch.")
                st.warning("Shared-machine measurements with documented exclusions; "
                           "not a production capacity guarantee.")
                link("Inspect workload evidence", "workload_evidence", "Workload measurements")


def about() -> None:
    st.html(visuals.banner("About", "About AgriSight",
                           "An independent, learning-oriented agricultural intelligence "
                           "project combining empirical findings with reproducible analytics "
                           "engineering.", "people"))
    st.html(visuals.section("Audiences", "Who it is designed to support",
                            "These are intended audiences, not claims of completed user "
                            "validation."))
    columns = st.columns(3)
    for column, (art, title, body) in zip(columns, [
            ("people", "Programme teams", ("Exploring agricultural questions with the "
             "limits of the evidence in plain view.")),
            ("search", "Analysts", ("Inspecting source data, denominators and exclusions "
             "behind each figure.")),
            ("scale", "Reviewers", ("Checking how conclusions were reached and what they "
             "cannot support."))]):
        with column, st.container(border=True, key="audience_"+art):
            st.html(visuals.icon(art, 48))
            st.markdown(f"#### {title}")
            st.write(body)
    st.html(visuals.section("Two layers", "One project, two ways to explore"))
    st.write("Start with the stakeholder summaries to understand the findings. "
             "Open Evidence & methods to examine calculations, choices and limitations.")
    st.info("Research and portfolio prototype. No live enrollment, client deployment, "
            "national inference or measured business impact is claimed.")
