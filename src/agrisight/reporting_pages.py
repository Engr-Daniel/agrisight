"""Stakeholder summaries over the same validated bundle as the technical explorer."""

import streamlit as st

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
    st.button(label, key=key, on_click=go,
              args=("Evidence & methods", view, indicator), width="stretch")


def survey_panel(bundle: dict) -> dict | None:
    panel = bundle["panels"]["survey"]
    if panel["status"] != "available":
        st.warning("Survey findings are unavailable. No summary figures are shown until "
                   "the reviewed evidence is available again.")
        return None
    st.caption(f"Source: {panel['origin']} | Reference: {panel['reference_period']}")
    return panel


def overview(bundle: dict) -> None:
    st.subheader("Agricultural evidence, made easier to explore")
    st.write("AgriSight brings agricultural survey findings and transparent analytical "
             "methods into one place. Built for programme teams, analysts and reviewers "
             "who want to understand what the available evidence can support.")
    actions = st.columns(2)
    actions[0].button("Explore agricultural insights", key="explore_insights", type="primary",
                      on_click=go, args=("Agricultural insights",), width="stretch")
    actions[1].button("Open technical evidence", key="open_evidence", on_click=go,
                      args=("Evidence & methods", "Survey findings"), width="stretch")
    st.subheader("The survey at a glance")
    panel = survey_panel(bundle)
    if panel:
        first, second = panel["records"]
        counts, areas = first["counts"], second["counts"]
        columns = st.columns(3)
        columns[0].metric("Household records", integer(counts["input_rows"]))
        columns[1].metric("Plot records", integer(areas["total_plots"]))
        columns[2].metric("Crop participation", percentage(first["values"]["proportion"]))
        st.caption(f"Participation: {integer(counts['numerator'])} yes responses / "
                   f"{integer(counts['denominator'])} valid household responses. "
                   "Households and plots are different units; these counts are not added.")
        st.info("Historical, unweighted sample findings. Not national estimates or current "
                "field conditions; population uncertainty is not estimated.")
    st.subheader("Choose what you want to understand")
    columns = st.columns(3)
    topics = [("Agricultural insights", "What does the released sample show?",
               "Read the crop-participation finding and the limits of plot-area records."),
              ("Engineering studies", "How were analytical methods tested?",
               "Explore separate synthetic matching and local workload studies."),
              ("Evidence & methods", "What supports each finding?",
               "Inspect definitions, denominators, exclusions and full-precision evidence.")]
    for column, (page, title, body) in zip(columns, topics):
        with column, st.container(border=True):
            st.markdown(f"#### {title}")
            st.write(body)
            st.button(page, key="topic_"+page, on_click=go, args=(page,),
                      width="stretch")
    st.subheader("Why the evidence is inspectable")
    st.write("Traceable sources. Independently reconciled calculations. Aggregate reporting "
             "that keeps survey findings and synthetic experiments separate.")
    st.caption("An independent research and portfolio prototype. Intended audiences are "
               "proposed users; no client deployments or business impact are claimed.")


def insights(bundle: dict) -> None:
    st.title("What the agricultural sample reveals")
    st.write("Two findings from the released NASS data, with their scope in view.")
    panel = survey_panel(bundle)
    if panel is None:
        return
    first, second = panel["records"]
    with st.container(border=True):
        st.subheader("Main-season crop participation")
        counts, values = first["counts"], first["values"]
        st.metric("Crop participation", percentage(values["proportion"]))
        if values["proportion"] is None:
            st.info("Participation is not defined because there are no valid responses.")
        else:
            st.write(f"{percentage(values['proportion'])} of valid household responses "
                     "reported growing crops in the main season.")
            st.bar_chart({"Response": ["Yes", "No"],
                          "Households": [counts["numerator"], counts["no_count"]]},
                         x="Response", y="Households", horizontal=True, color="#577B45",
                         alt="Counts of valid household responses reporting yes and no.")
        st.caption(f"{integer(counts['numerator'])} yes / {integer(counts['denominator'])} "
                   f"valid responses; {integer(counts['excluded_count'])} missing/invalid excluded.")
        st.warning("Unweighted released sample, not national or current prevalence. "
                   "No population confidence interval is available.")
        st.caption(f"Source: {panel['origin']} | {panel['reference_period']}")
        link("Inspect participation evidence", "participation_evidence", "Survey findings", "NASS-01")
    with st.container(border=True):
        st.subheader("What missing plot areas can change")
        counts, values = second["counts"], second["values"]
        st.metric("Missing area values", integer(counts["missing_areas"]))
        if counts["total_plots"]:
            st.progress(counts["observed_areas"]/counts["total_plots"],
                        text=f"{integer(counts['observed_areas'])} / "
                             f"{integer(counts['total_plots'])} plots have recorded area values")
        if second["status"] == "undefined":
            st.info("The plot roster is empty; its median and bounds are not defined.")
        elif second["status"] == "unbounded":
            st.info("The nonnegative missing-value model gives no finite upper median bound.")
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
        st.warning("Released labelled units; measurement lineage is unverified. These are "
                   "missing-value bounds, not confidence intervals or a national farm-size estimate.")
        st.caption(f"Source: {panel['origin']} | {panel['reference_period']}")
        link("Inspect area evidence", "area_evidence", "Survey findings", "NASS-02")


def engineering(bundle: dict) -> None:
    st.title("Testing the analytical foundations")
    st.write("Separate synthetic studies examine matching errors and local batch behavior. "
             "They do not describe survey respondents or an operational farmer registry.")
    columns = st.columns(2)
    for column, key, title in zip(columns, ("synthetic_quality", "synthetic_workload"),
                                   ("Synthetic matching study", "Local workload study")):
        panel = bundle["panels"][key]
        with column, st.container(border=True):
            st.subheader(title)
            st.caption(f"Source: {panel['origin']} | {panel['reference_period']}")
            if panel["status"] != "available":
                st.warning("Study evidence is unavailable; no result is shown.")
                continue
            if key == "synthetic_quality":
                row = next(r for r in panel["records"] if r["selectors"] == {
                    "seed": 303, "configuration": "Mixed", "baseline": "B1",
                    "measure": "duplicate_role"})
                st.caption("Mixed scenario · Seed303 · B1 · Duplicate role submissions")
                st.metric("Precision", percentage(row["values"]["precision"]))
                st.metric("Recall", percentage(row["values"]["recall"]))
                st.write("False links and missed repeats matter. Inspect both before "
                         "considering how matching rules might be used.")
                st.warning("Synthetic accuracy only. No field accuracy or automatic merging claim.")
                link("Inspect matching evidence", "matching_evidence", "Synthetic quality")
            else:
                row = next(r for r in panel["records"] if r["selectors"] == {
                    "events": 55000, "collision": False})
                st.metric("Submission events", integer(row["counts"]["events"]))
                if row["status"] == "success":
                    st.metric("Median batch time (seconds)",
                              decimal(row["values"]["timing"]["median"], 3))
                else:
                    st.info("This workload has no successful timing result; no time is shown.")
                st.write("Submission events are not distinct people or roles. "
                         "This study measures a specific bounded-key local batch.")
                st.warning("Shared-machine measurements with documented exclusions; "
                           "not a production capacity guarantee.")
                link("Inspect workload evidence", "workload_evidence", "Workload measurements")


def about() -> None:
    st.title("About AgriSight")
    st.write("An independent, learning-oriented agricultural intelligence project combining "
             "empirical findings with reproducible analytics engineering.")
    st.subheader("Who it is designed to support")
    st.write("Programme teams exploring agricultural questions, analysts inspecting "
             "source data and reviewers checking how conclusions were reached. "
             "These are intended audiences, not claims of completed user validation.")
    st.subheader("One project, two ways to explore")
    st.write("Start with the stakeholder summaries to understand the findings. "
             "Open Evidence & methods to examine calculations, choices and limitations.")
    st.info("Research and portfolio prototype. No live enrollment, client deployment, "
            "national inference or measured business impact is claimed.")
