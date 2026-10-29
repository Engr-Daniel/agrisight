"""Read-only Streamlit views over freshly validated aggregate evidence."""

from datetime import datetime
from pathlib import Path

import streamlit as st

from agrisight import reporting_adapter

VIEWS = {"Survey findings": "survey", "Synthetic quality": "synthetic_quality",
         "Workload measurements": "synthetic_workload"}
MEASURES = {"same_person": "Same person", "duplicate_role": "Duplicate role submissions",
            "quality": "All four field rules (micro)", "missing_name": "Missing name",
            "missing_contact": "Missing contact", "name_whitespace": "Name whitespace",
            "contact_whitespace": "Contact whitespace"}
COUNT_LABELS = {"input_rows": "Released household records", "numerator": "Yes responses",
                "denominator": "Valid responses", "no_count": "Answered no (code 2)",
                "missing_count": "Missing responses", "invalid_count": "Invalid responses",
                "excluded_count": "Excluded responses", "total_plots": "Eligible plot records",
                "observed_areas": "Known area values", "missing_areas": "Missing area values",
                "events": "Submission events", "people": "True synthetic people",
                "intended_roles": "Intended roles", "tp": "True positives (TP)",
                "fp": "False positives (FP)", "fn": "Missed positives (FN)",
                "tn": "True negatives (TN)", "universe": "Evaluation universe",
                "true_pairs_or_labels": "Actual positives (TP + FN)",
                "predicted_pairs_or_labels": "Predicted positives (TP + FP)",
                "candidate_pairs": "Candidate pairs", "pair_budget": "Candidate budget"}


def integer(value: int | None) -> str:
    return "Not defined" if value is None else f"{value:,}"


def percentage(value: float | None) -> str:
    if value is None:
        return "Not defined"
    return "<0.01%" if 0 < value*100 < 0.01 else f"{value*100:.2f}%"


def decimal(value: float | None, places: int, unbounded: bool = False) -> str:
    if value is None:
        return "Unbounded" if unbounded else "Not defined"
    return f"{value:,.{places}f}"


def build_time(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M:%S")


def count_table(counts: dict) -> None:
    st.table([{"Measure": COUNT_LABELS.get(key, key.replace("_", " ").capitalize()),
               "Count": integer(value)}
              for key, value in counts.items()])


def evidence(panel: dict, row: dict) -> None:
    with st.expander("Evidence & provenance"):
        st.caption("Full-precision aggregate values and reviewed source/model fingerprints.")
        st.json({"selected_cell": row["selectors"], "counts": row["counts"],
                 "values": row["values"], "units": row["units"], "status": row["status"],
                 "provenance": panel["provenance"]})


def survey(panel: dict) -> None:
    choice = st.selectbox("Indicator", ("NASS-01", "NASS-02"), key="indicator",
                          format_func=lambda v: {"NASS-01": "Main-season crop participation",
                                                 "NASS-02": "Released plot-area median bounds"}[v])
    row = next(r for r in panel["records"] if r["id"] == choice)
    st.warning(" ".join(panel["limitations"] if choice == "NASS-02"
                        else panel["limitations"][:1]))
    counts, values = row["counts"], row["values"]
    if choice == "NASS-01":
        st.subheader("Main-season crop participation")
        columns = st.columns(3)
        columns[0].metric("Crop participation", percentage(values["proportion"]))
        columns[1].metric("Yes responses", integer(counts["numerator"]))
        columns[2].metric("Valid household responses", integer(counts["denominator"]))
        st.write(f"{integer(counts['numerator'])} yes / {integer(counts['denominator'])} "
                 "valid household responses.")
        st.caption("One record per released agricultural household. Unweighted sample "
                   "description, not national or current prevalence; uncertainty not estimated.")
        if row["status"] == "undefined":
            st.info("Participation is not defined because there are no valid responses.")
    else:
        st.subheader("Median bounds for the released plot-area field")
        columns = st.columns(3)
        for column, label, key in zip(columns, ("Lower bound (labelled m²)",
                                                "Upper bound (labelled m²)",
                                                "Bound width (labelled m²)"),
                                      ("full_roster_lower_m2", "full_roster_upper_m2", "width_m2")):
            column.metric(label, decimal(values[key], 2, row["status"] == "unbounded" and
                                         key == "full_roster_upper_m2"))
        st.write("Known-area-only median (a separate reference): "
                 f"{decimal(values['observed_only_median_m2'], 2)} labelled m².")
        st.caption("One record per main-season plot, not a household farm total. "
                   "Bounds allow unknown nonnegative values; they are not confidence intervals. "
                   "Measurement lineage is unverified; this is not national median farm size.")
        if row["status"] == "undefined":
            st.info("Median and bounds are not defined because the roster is empty.")
        elif row["status"] == "unbounded":
            st.info("The missing-value model gives no finite upper bound. "
                    "An unbounded endpoint is different from an undefined or recorded zero value.")
        elif counts["missing_areas"] and values["width_m2"] == 0:
            st.info("The bounds coincide under the nonnegative missing-value model. "
                    "This does not establish accuracy of known measurements.")
    st.caption(f"Source: {panel['origin']}")
    count_table(counts)
    evidence(panel, row)


def quality(panel: dict) -> None:
    seed = st.selectbox("Evaluation seed", (303, 404, 505), key="seed")
    config = st.selectbox("Scenario", ("Clean", "Exact-repeat", "Mixed"), index=2, key="scenario")
    baseline = st.selectbox("Matching baseline", ("B0", "B1"), index=1, key="baseline")
    mode = st.radio("Evaluation", ("Matching", "Field quality"), key="evaluation",
                    horizontal=True)
    measure = st.selectbox("Relation" if mode == "Matching" else "Quality rule",
                           ("same_person", "duplicate_role") if mode == "Matching"
                           else ("quality", *reporting_adapter.RULES),
                           index=1 if mode == "Matching" else 0,
                           key="relation" if mode == "Matching" else "rule",
                           format_func=MEASURES.__getitem__)
    selectors = {"seed": seed, "configuration": config, "baseline": baseline, "measure": measure}
    row = next(r for r in panel["records"] if r["selectors"] == selectors)
    c, v = row["counts"], row["values"]
    st.subheader(MEASURES[measure])
    st.caption("B0: raw exact name/contact agreement. B1: trim whitespace and casefold "
               "both tokens before exact agreement. No automatic merging.")
    columns = st.columns(3)
    for column, key, label in zip(columns, ("events", "people", "intended_roles"),
                                  ("Submission events", "True synthetic people", "Intended roles")):
        column.metric(label, integer(c[key]))
    unit = ("unordered event pairs" if mode == "Matching" else
            "event-rule cells" if measure == "quality" else "events")
    st.write(f"Evaluation universe: {integer(c['universe'])} {unit}.")
    st.caption("A person may hold both roles. A same-person cross-role pair is valid; "
               "it is not a repeated role submission." if mode == "Matching" else
               "Field rules are identical across baselines and concern inserted rule families. "
               "Their scores do not measure identity matching or unseen defect types.")
    columns = st.columns(3)
    for column, key, label in zip(columns, ("precision", "recall", "false_positive_rate"),
                                  ("Precision", "Recall", "False-positive rate")):
        column.metric(label, percentage(v[key]))
    denominators = {"Precision": c["tp"]+c["fp"], "Recall": c["tp"]+c["fn"],
                    "False-positive rate": c["fp"]+c["tn"]}
    st.caption("Denominators - " + "; ".join(
        f"{label}: {integer(n)}" for label, n in denominators.items()) + ".")
    reasons = {"Precision": "no predicted positives", "Recall": "no actual positives",
               "False-positive rate": "no actual negatives"}
    for label, n in denominators.items():
        if not n:
            st.info(f"{label} is not defined: {reasons[label]}.")
    st.caption("TP = correctly flagged positives; FP = false flags; FN = missed positives; "
               "TN = correctly unflagged negatives. Actual positives = TP + FN; "
               "predicted positives = TP + FP. Synthetic accuracy does not establish field accuracy.")
    st.caption(f"Source: {panel['origin']}")
    count_table({k: c[k] for k in reporting_adapter.METRIC_COUNTS})
    evidence(panel, row)


def workload(panel: dict) -> None:
    cells = {f"{r['selectors']['events']}:{int(r['selectors']['collision'])}": r
             for r in panel["records"]}

    def label(key: str) -> str:
        selectors = cells[key]["selectors"]
        return ("Collision" if selectors["collision"] else "Bounded groups") + " / " + \
            integer(selectors["events"]) + " events"

    selected = st.selectbox("Workload", tuple(cells), index=tuple(cells).index("55000:0"),
                            key="workload", format_func=label)
    mode = st.radio("Measurement", ("timing", "traced_allocation"), key="measurement",
                    format_func=lambda k: "Batch time" if k == "timing" else "Traced allocation",
                    horizontal=True)
    row = cells[selected]
    st.subheader(label(selected))
    st.caption(f"Source: {panel['origin']}")
    count_table(row["counts"])
    st.caption("Events are submissions, not necessarily distinct people or intended roles. "
               "Collision diagnostics are separate from bounded-group scaling results. "
               "Timing does not establish matching correctness or justify automatic merging.")
    if row["status"] == "candidate_budget_exceeded":
        st.warning("Rejected: candidate budget exceeded. "
                   f"{integer(row['counts']['candidate_pairs'])} potential pairs / "
                   f"{integer(row['counts']['pair_budget'])} allowed.")
        st.info("Timing and traced allocation are unavailable for this rejected batch; "
                "they are not zero measurements.")
    elif row["status"] == "success":
        summary = row["values"][mode]
        unit, places = ("seconds", 3) if mode == "timing" else ("MiB", 2)
        st.caption("Validation + candidate guard + B1 detection. Generation, imports, process "
                   "startup, hashing, SQL correctness checks and I/O excluded. Shared-machine "
                   "load was not controlled." if mode == "timing" else
                   "Peak traced Python allocation after generation; existing inputs, interpreter "
                   "baseline and native memory excluded. Not process RSS or total RAM. "
                   "These runs are separate from timing repetitions.")
        columns = st.columns(3)
        for column, key in zip(columns, ("median", "minimum", "maximum")):
            column.metric(f"{key.capitalize()} ({unit})", decimal(summary[key], places))
        st.caption(f"Sample standard deviation: {decimal(summary['sample_stdev'], places)} "
                   f"{unit}. Every measured repetition retained; warm-up excluded.")
        st.table([{"Repetition": i, unit: decimal(value, places)}
                  for i, value in enumerate(summary["values"], 1)])
        st.caption(f"Source: {panel['origin']} | Stored measured repetitions ({unit})")
        st.bar_chart({"Repetition": list(range(1, len(summary["values"])+1)),
                      unit: summary["values"]}, x="Repetition", y=unit, sort=False,
                     x_label="Measured repetition", y_label=unit,
                     alt=f"{panel['origin']}: recorded repetition values in {unit}.")
    else:
        st.error("Unsupported measurement status. Revalidate the evidence.")
    evidence(panel, row)


def run(root: Path) -> None:
    st.set_page_config(page_title="AgriSight evidence explorer", layout="wide")
    st.title("AgriSight evidence explorer")
    st.write("Read the findings, their denominators and their limits.")
    st.sidebar.title("AgriSight")
    st.sidebar.caption("Local, read-only prototype")
    view = st.sidebar.radio("Evidence view", tuple(VIEWS), key="view")
    try:
        # Revalidate on every interaction; no session-state or cached evidence fallback.
        bundle = reporting_adapter.build_bundle(root)
    except (OSError, ValueError, KeyError, TypeError):
        st.error("Evidence unavailable. Restore the reviewed reporting inputs and try again.")
        return
    for title, key in VIEWS.items():
        st.sidebar.caption(f"{title}: {bundle['panels'][key]['status']}")
    panel = bundle["panels"][VIEWS[view]]
    st.info(f"Source: {panel['origin']}")
    st.caption(f"Reference: {panel['reference_period']} | "
               f"Evidence observed: {panel['observed_date']} | "
               f"Bundle built (UTC): {build_time(bundle['built_at_utc'])}")
    st.caption("A new build time does not update the survey period or experiment evidence.")
    if VIEWS[view] != "survey":
        st.warning(" ".join(panel["limitations"]))
    if panel["status"] != "available":
        st.error("Evidence unavailable. Revalidate the reviewed aggregate artifacts. "
                 "Other independently valid views may remain available.")
        return
    {"survey": survey, "synthetic_quality": quality,
     "synthetic_workload": workload}[VIEWS[view]](panel)
