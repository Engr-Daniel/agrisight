"""Seed channels and overlap, with record grain and variety limits explicit."""

import pandas as pd
import streamlit as st

from agrisight.water_management import bars, rate


def show(bundle: dict) -> None:
    st.subheader("Seed sources")
    st.write("Which seed channels are reported for temporary household–crop records, and which occur together?")
    if bundle["status"] != "available":
        st.info("Reviewed seed-source evidence is unavailable. Other agricultural findings remain available.")
        return
    if bundle["origin"] == "TEST FIXTURE":
        st.warning("TEST FIXTURE — illustrative seed records, not survey findings.")
    view = st.selectbox("Explore seed records", ("Sources", "Source combinations"), key="seed_view")
    unit = st.radio("Show seed values as", ("Percentages", "Record counts"), horizontal=True, key="seed_unit")
    c, sources = bundle["counts"], bundle["sources"]
    st.caption(f'{c["eligible_records"]:,} eligible temporary household–crop seed records from '
               f'{c["represented_households"]:,} represented households. A household can contribute several crop records. '
               "NBS NASS 2023, April–October 2022; unweighted sample, not national prevalence.")
    if view == "Sources":
        rows = [{"label": s["label"], "count": s["yes"], "share": s["share"]} for s in sources]
        denominators = {s["denominator"] for s in sources}
        if len(denominators) == 1:
            st.caption(f'Each source percentage uses {next(iter(denominators)):,} valid yes/no record responses.')
        else:
            st.caption("Source percentage denominators differ; see valid responses and exclusions in the table.")
        # Percentage bars use their own shares; count bars use a common eligible-record scale.
        st.html(bars(rows, c["eligible_records"], unit, "agri-seed-chart", "eligible household–crop records"))
        valid = [s for s in sources if s["denominator"]]
        if valid:
            top = max(valid, key=lambda s: s["yes"])
            st.write(f'{top["label"]} is reported on {top["yes"]:,} of {top["denominator"]:,} valid '
                     f'household–crop responses ({rate(top["share"])}). This counts crop-specific records, not unique households.')
        st.write("Sources can overlap. Do not add source counts or percentages to count unique households. These are recorded channels, not evidence of affordability, seed quality or unmet demand.")
        table = [{"Source": s["label"], "Yes records": s["yes"], "No records": s["no"],
                  "Valid responses": s["denominator"], "Missing": s["missing"], "Invalid": s["invalid"],
                  "Share": rate(s["share"])} for s in sources]
    else:
        combo = bundle["combinations"]
        denominator = combo["denominator"]
        rows = []
        for r in sorted(combo["rows"], key=lambda r: -r["records"]):
            label = ("Other combinations (pooled)" if r["mask"] is None else
                     " + ".join(s["label"] for i, s in enumerate(sources) if r["mask"] & (1 << i)))
            if r["mask"]:
                label += " (only)"
            rows.append({"label": label or "No source selected (all five zero)", "count": r["records"], "share": r["share"]})
        st.caption(f'Complete-vector denominator: {denominator:,} records with five valid source responses; '
                   f'{combo["excluded"]:,} incomplete/invalid records excluded. Chart shows up to six published groups; '
                   "table includes the pooled remainder. Rare combinations are not individually exposed.")
        if rows:
            st.html(bars(rows[:6], denominator, unit, "agri-seed-chart", "complete household–crop records"))
        else:
            st.info("Combination values are withheld or unavailable because too few complete records support the display.")
        st.write("Published combination groups are mutually exclusive for complete records. Up to six frequent named combinations are shown; all others are pooled. All-zero selections do not establish that no seeds were used.")
        table = [{"Combination": r["label"], "Records": r["count"], "Share": rate(r["share"])} for r in rows]
    with st.expander("Read the complete seed table"):
        st.dataframe(pd.DataFrame(table), hide_index=True, width="stretch")
    st.caption(f'{c["excluded_permanent_records"]:,} permanent/continuous seed records are excluded. '
               f'{c["crop_yes_without_temporary_seed_record"]:,} crop-yes households have no temporary seed record; '
               f'{c["temporary_seed_households_without_crop_yes"]:,} represented households lack a crop-yes response. '
               "This seed roster is not assumed identical to the crop portfolio roster.")
    st.info("Variety and certification percentages are not shown because the released variety definitions need confirmation. Do not interpret source channels as modern/improved-seed adoption or certification.")
    st.write("Use the channel mix to frame follow-up about how seeds are obtained for recorded crops. Quantities, commercial demand, seed quality and programme effects require separate evidence.")
