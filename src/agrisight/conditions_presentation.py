"""Question-led FC1 views: composition, ordered dots, paired dots and heatmaps."""

from html import unescape

import altair as alt
import pandas as pd
import streamlit as st

SOURCE = "Data context: NBS NASS 2023 · April–October 2022 context."


def rate(value: float | None) -> str:
    return "Undefined" if value is None else f"{value:.2%}"


def chart_style(chart):
    return chart.configure_view(stroke=None).configure(background="#f6f7f0").configure_axis(
        labelColor="#203c2d", titleColor="#203c2d", gridColor="#dfe6d6").configure_legend(labelColor="#203c2d")


def dots(rows: list[dict], counts: bool = False, series: bool = False) -> alt.Chart:
    frame = pd.DataFrame(rows, columns=["label", "count", "share", "valid", "series"])
    x = alt.X("count:Q", title="Recorded responses", scale=alt.Scale(zero=True)) if counts else alt.X(
        "share:Q", title="Share of valid responses", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format=".0%", tickCount=5))
    chart = alt.Chart(frame).mark_point(filled=True, size=100, color="#357047").encode(
        x=x, y=alt.Y("label:N", title=None, sort=list(dict.fromkeys(r["label"] for r in rows)), axis=alt.Axis(labelLimit=160)),
        tooltip=[alt.Tooltip("label:N", title="Category"), alt.Tooltip("count:Q", title="Responses", format=","),
                 alt.Tooltip("valid:Q", title="Valid denominator", format=","),
                 alt.Tooltip("share:Q", title="Share", format=".2%")])
    if series:
        chart = chart.encode(color=alt.Color("series:N", title=None, scale=alt.Scale(
            domain=["Sales", "Storage"], range=["#174d36", "#bd8b24"]), legend=alt.Legend(orient="bottom")),
            shape=alt.Shape("series:N", title=None), tooltip=[alt.Tooltip("label:N", title="Crop"),
                alt.Tooltip("series:N", title="Report"), alt.Tooltip("count:Q", title="Yes records", format=","),
                alt.Tooltip("valid:Q", title="Valid denominator", format=","), alt.Tooltip("share:Q", title="Share", format=".2%")])
    return chart.properties(height=max(170, len({r["label"] for r in rows})*30))


def table(summary: dict) -> None:
    st.caption(f'{summary["valid"]:,} valid responses from {summary["eligible"]:,} eligible records; '
               f'{summary["missing"]:,} missing and {summary["invalid"]:,} invalid excluded from percentages.')
    st.dataframe(pd.DataFrame([{"Response": r["label"], "Records": r["count"], "Share": rate(r["share"])}
                               for r in summary["rows"]]), hide_index=True, width="stretch")


def dot_rows(summary: dict) -> list[dict]:
    return [{**r, "valid": summary["valid"], "series": ""} for r in summary["rows"]]


def land(bundle: dict, counts: bool) -> None:
    st.markdown("#### Land arrangements and reaching plots")
    selection = st.selectbox("Explore land and travel", ("Tenure", "Travel time", "Transport"), key="fc_land")
    key = {"Tenure": "tenure", "Travel time": "travel", "Transport": "transport"}[selection]
    data = bundle["land"]
    summary = data[key]
    if summary["valid"]:
        leading = max(summary["rows"], key=lambda r: r["count"])
        st.write(f'One of the largest recorded categories is {leading["label"]}: {leading["count"]:,} '
                 f'of {summary["valid"]:,} valid plot responses ({rate(leading["share"])}).')
    if key == "tenure" and summary["valid"]:
        short = ["Owned by HH member", "Rented", "Other", "Free family land", "Free community land", "Other free-use land"]
        rows = [{**r, "category": short[i]} for i, r in enumerate(summary["rows"])]
        chart = alt.Chart(pd.DataFrame(rows)).mark_arc(innerRadius=58, outerRadius=95).encode(
            theta=alt.Theta("count:Q", stack=True), order=alt.Order("code:Q"),
            color=alt.Color("category:N", title=None, sort=short, scale=alt.Scale(range=["#174d36", "#357047", "#b89446", "#70985b", "#adc28c", "#d4ddb9"]),
                            legend=alt.Legend(orient="bottom", columns=1, labelLimit=260)),
            tooltip=[alt.Tooltip("label:N", title="Tenure"), alt.Tooltip("count:Q", title="Plot records", format=","),
                     alt.Tooltip("share:Q", title="Share of valid plots", format=".2%")]).properties(height=390)
        st.altair_chart(chart_style(chart), width="stretch")
        st.write("The ring shows how valid plot records are divided between tenure arrangements. "
                 "Free-use land remains separate from household ownership; this is not evidence of legal title or tenure security.")
    else:
        st.altair_chart(chart_style(dots(dot_rows(summary), counts)), width="stretch")
    if key == "travel":
        with st.expander("Understanding these figures - travel time"):
            st.write("Travel bands stay in their questionnaire order. The open-ended final band prevents a reliable average-minute calculation. "
                     "These are journeys from dwellings to plots, not to markets or agricultural services.")
        st.caption(f'{data["on_dwelling"]:,} on-dwelling plots skip travel; {data["unknown_transport"]:,} plots have unknown transport eligibility. '
                   f'{data["outside_travel_answers"]:,} travel entries outside the eligible subset are excluded.')
    table(summary)
    st.caption(SOURCE + " Counting unit: plot records; all roster plot types included.")


def difficulties(bundle: dict, counts: bool) -> None:
    st.markdown("#### Harvest difficulties and reported losses")
    data = bundle["difficulties"]
    branch_name = st.selectbox("Explore harvest response branch", ("nonvegetable", "vegetable"),
        format_func=lambda v: "Non-vegetable recorded branch" if v == "nonvegetable" else "Vegetable recorded branch", key="fc_branch")
    branch = next(b for b in data["branches"] if b["name"] == branch_name)
    question = st.selectbox("Explore harvest difficulties", ("Harvest reported", "No-harvest reasons", "Unharvested area due to shocks", "Shock reasons"), key="fc_difficulty")
    st.caption("Counting unit: temporary crop-plot responses in the selected branch.")
    with st.expander("Harvest response coverage"):
        st.caption(f'{data["temporary_records"]:,} temporary crop-plot records; {data["excluded_permanent"]:,} permanent records excluded. '
               f'{data["unassigned"]:,} temporary records have neither harvest branch; {data["ambiguous"]:,} have both and are excluded. '
               "Branch membership follows recorded responses, not an inferred crop classification.")
    if question in ("Harvest reported", "Unharvested area due to shocks"):
        summary = branch["harvest" if question == "Harvest reported" else "shocks"]
        yes = summary["rows"][0]
        st.write(f'{yes["count"]:,} of {summary["valid"]:,} valid eligible responses report yes '
                 f'({rate(yes["share"])}); see the question and eligibility notes before interpretation.')
        st.altair_chart(chart_style(dots(dot_rows(summary), counts)), width="stretch")
        table(summary)
    else:
        reasons = branch["no_harvest_reasons" if question == "No-harvest reasons" else "shock_reasons"]
        rows = [{"label": r["label"], "count": r["rows"][1]["count"], "share": r["rows"][1]["share"], "valid": r["valid"], "series": ""} for r in reasons]
        available = [r for r in rows if r["share"] is not None]
        if available:
            leading = max(available, key=lambda r: r["share"])
            st.write(f'One of the most frequently selected reasons is {leading["label"]}: '
                     f'{leading["count"]:,} of {leading["valid"]:,} valid responses ({rate(leading["share"])}). '
                     "This is a reported reason, not independently measured causation.")
        st.altair_chart(chart_style(dots(rows, counts)), width="stretch")
        st.dataframe(pd.DataFrame([{"Reason": r["label"], "Yes": r["rows"][1]["count"], "Valid": r["valid"],
            "Eligible": r["eligible"], "Missing": r["missing"], "Invalid": r["invalid"], "Share": rate(r["rows"][1]["share"])} for r in reasons]), hide_index=True, width="stretch")
        st.caption("Reasons can overlap. Each percentage uses that reason's valid 0/1 responses within the affected subset; missing is not no.")
    if question in ("Unharvested area due to shocks", "Shock reasons"):
        st.caption(f'Eligible only after harvest=yes and completion=no. {branch["outside_shock_answers"]:,} shock entries outside this subset are excluded. '
                   f'Completion has {branch["completion"]["missing"]:,} missing and {branch["completion"]["invalid"]:,} invalid responses among harvested branch records.')
    st.caption("No harvest can reflect timing or deferral; it does not automatically mean crop failure.")
    with st.expander("Understanding these figures - harvest responses"):
        st.write("No harvest can reflect timing or a deferred harvest; it does not automatically mean crop failure. "
                 "Reported drought, flood or pests frame questions for investigation, rather than establish causes or measured damage.")
    st.caption(SOURCE + " Counting unit: temporary crop-plot responses. Broad loss reports appear in Sales & storage.")


def destinations(bundle: dict, counts: bool) -> None:
    st.markdown("#### Crop sales, storage and broad loss reports")
    data = bundle["destinations"]
    st.write("Across all recorded harvested household–crop rows, " + "; ".join(
        f'{name}: {data[name]["rows"][0]["count"]:,}/{data[name]["valid"]:,} valid responses '
        f'({rate(data[name]["rows"][0]["share"])})' for name in ("sales", "storage", "losses")) + ".")
    mode = st.selectbox("Explore crop destinations", ("Crop comparison", "Sales and storage overlap", "Broad loss reports"), key="fc_destination")
    if mode == "Crop comparison":
        choices = [{"code": 0, "label": "Overview: 10 most recorded crops", **{k: data[k] for k in ("sales", "storage", "losses")}}, *data["crops"]]
        code = st.selectbox("Focus harvested crop", [c["code"] for c in choices],
                            format_func=lambda code: next(c["label"] for c in choices if c["code"] == code), key="fc_crop")
        selected = [c for c in choices if c["code"] == code] if code else sorted(data["crops"], key=lambda c: -c["sales"]["eligible"])[:10]
        if not selected:
            selected = [{**choices[0], "label": "All recorded harvested crops"}]
        rows = [{"label": c["label"], "series": name.title(), "count": c[name]["rows"][0]["count"], "share": c[name]["rows"][0]["share"], "valid": c[name]["valid"]}
                for c in selected for name in ("sales", "storage")]
        st.altair_chart(chart_style(dots(rows, counts, True)), width="stretch")
        st.caption("Default: up to 10 crops with the most recorded destination rows, not the highest percentages. "
                   f'{data["omitted_crop_categories"]:,} crop categories lack at least 30 valid responses per field and are omitted from crop detail. '
                   "Each dot uses its own field-valid household–crop denominator; these are not shares of crop output.")
        st.dataframe(pd.DataFrame([{"Crop": c["label"], "Report": n.title(), "Yes": c[n]["rows"][0]["count"], "Valid": c[n]["valid"],
            "Missing": c[n]["missing"], "Invalid": c[n]["invalid"], "Share": rate(c[n]["rows"][0]["share"])} for c in selected for n in ("sales", "storage")]), hide_index=True, width="stretch")
    elif mode == "Sales and storage overlap":
        joint = data["overlap"]
        rows = [{"Sales": "Yes" if c["sales"] == 1 else "No", "Storage": "Yes" if c["storage"] == 1 else "No", "Records": c["count"],
                 "Share": c["count"]/joint["valid"] if joint["valid"] else None} for c in joint["cells"]]
        chart = alt.Chart(pd.DataFrame(rows)).mark_rect(cornerRadius=4).encode(
            x=alt.X("Sales:N", title="Reported sales", sort=["Yes", "No"]), y=alt.Y("Storage:N", title="Reported storage", sort=["Yes", "No"]),
            color=alt.Color("Share:Q", scale=alt.Scale(domain=[0, 1], scheme="greens"), legend=alt.Legend(format=".0%")),
            tooltip=["Sales:N", "Storage:N", alt.Tooltip("Records:Q", format=","), alt.Tooltip("Share:Q", format=".2%")]).properties(height=220)
        st.altair_chart(chart_style(chart), width="stretch")
        st.caption(f'{joint["valid"]:,} records valid for both questions; {joint["excluded"]:,} excluded. Sales and storage are not mutually exclusive.')
        st.dataframe(pd.DataFrame(rows).assign(Share=[rate(r["Share"]) for r in rows]), hide_index=True, width="stretch")
    else:
        st.altair_chart(chart_style(dots(dot_rows(data["losses"]), counts)), width="stretch")
        table(data["losses"])
        st.write("This question covers losses during or after harvest, including post-harvest activities, transport and storage. "
                 "It is a report of any loss, not the proportion of output lost or a post-harvest-only loss rate.")
    with st.expander("Understanding these figures - sales and storage"):
        st.write("Sales reports describe participation since harvest; storage describes unprocessed crop retained at interview. "
                 "Neither establishes profitability, market access or sufficient storage capacity.")
    with st.expander("Read all-crop response denominators"):
        for key in ("sales", "storage", "losses"):
            st.markdown(f"**{key.title()}**")
            table(data[key])
    st.caption(SOURCE + " Grain: harvested temporary household–crop records; never a plot-level join.")


def input_cells(records: list[dict]) -> list[dict]:
    """Distinct input types must never share a heatmap row after shortening labels."""
    names = {15: "Other organic fertilizer", 21: "Other pesticides"}
    return [{"Input": names.get(r["code"], unescape(r["label"].split(":")[-1].strip())),
             "Input type": unescape(r["label"]), "Status": s["label"], "Records": s["count"],
             "Share": s["share"], "Denominator": r["records"]} for r in records for s in r["statuses"]]


def inputs(bundle: dict) -> None:
    st.markdown("#### Recorded inputs and quantity information gaps")
    total = bundle["counts"]["inputs"]
    missing = sum(r["statuses"][2]["count"] for r in bundle["inputs"])
    st.write(f'{missing:,} of {total:,} recorded household–input rows lack a quantity '
             f'({rate(missing/total if total else None)}).')
    if bundle["inputs"]:
        leading = max(bundle["inputs"], key=lambda r: r["statuses"][2]["count"])
        st.write(f'The largest number of missing quantities is in {unescape(leading["label"])}: '
                 f'{leading["statuses"][2]["count"]:,} of its {leading["records"]:,} recorded rows '
                 f'({rate(leading["statuses"][2]["share"])}). This identifies a measurement follow-up, not low input use.')
    rows = input_cells(bundle["inputs"])
    chart = alt.Chart(pd.DataFrame(rows, columns=["Input", "Input type", "Status", "Records", "Share", "Denominator"])).mark_rect(cornerRadius=2).encode(
        x=alt.X("Status:N", title=None, sort=["Positive", "Zero", "Missing", "Invalid"], axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Input:N", title=None, sort=list(dict.fromkeys(r["Input"] for r in rows)), axis=alt.Axis(labelLimit=150)),
        color=alt.Color("Share:Q", title="Within input type", scale=alt.Scale(domain=[0, 1], scheme="greens"), legend=alt.Legend(orient="bottom", format=".0%")),
        tooltip=["Input type:N", "Status:N", alt.Tooltip("Records:Q", format=","), alt.Tooltip("Denominator:Q", format=","), alt.Tooltip("Share:Q", format=".2%")]).properties(height=max(220, len(bundle["inputs"])*29))
    st.altair_chart(chart_style(chart), width="stretch")
    st.caption("Each row sums to 100% of that input's recorded household–input rows. Colour shows quantity-status share, not amount used. Hover for figures.")
    st.dataframe(pd.DataFrame([{"Input": unescape(r["label"]), "Recorded rows": r["records"],
        **{s["label"]: s["count"] for s in r["statuses"]}} for r in bundle["inputs"]]), hide_index=True, width="stretch")
    st.caption("Missing quantity is not zero use. Amounts are not compared across input types.")
    with st.expander("Understanding these figures - input quantities"):
        st.write("Missing quantities are information gaps, not zero use. Absent input records do not prove non-use. "
                 "The release lacks a matching quantity-unit field, so amounts are not added or compared across inputs.")
    st.caption(SOURCE + " Counting unit: household–input records. Rainy-season input reporting.")


def show(bundle: dict) -> None:
    st.subheader("Farming conditions, harvest and input records")
    if bundle["status"] != "available":
        st.info("Reviewed farming-condition evidence is unavailable. These findings are hidden until their aggregate is verified.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative records, not survey findings.")
    counts = st.radio("Show farming-condition dot charts as", ("Percentages", "Record counts"), horizontal=True, key="fc_unit") == "Record counts"
    tabs = st.tabs(["Land & travel", "Harvest difficulties", "Sales & storage", "Input records"])
    for tab, render in zip(tabs[:3], (land, difficulties, destinations), strict=True):
        with tab:
            render(bundle, counts)
    with tabs[3]:
        inputs(bundle)


def show_topic(bundle: dict, topic: str) -> None:
    """Render one subject inside the site's grouped navigation."""
    if bundle["status"] != "available":
        st.info("Reviewed farming-condition evidence is unavailable. These findings are hidden until their aggregate is verified.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative records, not survey findings.")
    if topic == "inputs":
        inputs(bundle)
    else:
        counts = st.radio("Chart values", ("Percentages", "Record counts"), horizontal=True,
                          key=f"fc_{topic}_unit") == "Record counts"
        {"land": land, "harvest": difficulties, "markets": destinations}[topic](bundle, counts)
