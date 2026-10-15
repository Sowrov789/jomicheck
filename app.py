"""JomiCheck Lite: a beginner-friendly Streamlit demo for LandTech P5."""

from html import escape
import streamlit as st

from data_logic import find_plot_records, get_unique_plot_ids, get_warnings, load_records


st.set_page_config(
    page_title="JomiCheck Lite | LandTech 2026",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
      .stApp { background: #f5f8f7; }
      .block-container { max-width: 1180px; padding-top: 1.8rem; padding-bottom: 3rem; }
      h1, h2, h3 { font-family: 'Trebuchet MS', Arial, sans-serif; color: #133c35; }
      p, label, .stMarkdown, div[data-testid='stMetricValue'] { font-family: Arial, sans-serif; }
      .eyebrow { color: #b5e9d8; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; font-size: .75rem; margin-bottom: .65rem; }
      .hero { background: linear-gradient(120deg, #123e36 0%, #176858 65%, #24856b 100%); color: white; padding: 2rem 2.1rem; border-radius: 22px; margin-bottom: 1rem; box-shadow: 0 12px 32px rgba(16, 70, 57, .12); }
      .hero h1 { color: #ffffff !important; font-size: clamp(1.9rem, 4vw, 2.75rem); line-height: 1.12; margin: 0 0 .65rem 0; font-weight: 800; }
      .hero p { color: #e1f5ed; font-size: 1.02rem; max-width: 780px; margin: 0; line-height: 1.65; }
      .hero-chip { display: inline-block; margin-top: 1.1rem; border: 1px solid rgba(255,255,255,.35); color: #e9fff5; border-radius: 999px; padding: .35rem .72rem; font-size: .79rem; font-weight: 600; }
      .section-kicker { color: #35836d; text-transform: uppercase; letter-spacing: .1em; font-size: .73rem; font-weight: 800; margin-bottom: .3rem; }
      .section-title { color: #163e36; font-family: 'Trebuchet MS', Arial, sans-serif; font-size: 1.35rem; font-weight: 800; margin-bottom: .2rem; }
      .muted { color: #607770; font-size: .92rem; }
      .sample-label { font-size: .82rem; font-weight: 700; color: #42665c; margin: .35rem 0 .55rem 0; }
      .result-heading { border-bottom: 1px solid #dfe9e5; padding-bottom: .65rem; margin-bottom: 1rem; }
      .timeline-date { font-size: .78rem; color: #528174; font-weight: 700; margin-bottom: .15rem; }
      .timeline-owner { font-weight: 700; color: #173f36; }
      .timeline-event { color: #607770; font-size: .9rem; }
      div[data-testid='stMetric'] { background: #ffffff; border: 1px solid #e1ebe7; padding: .85rem 1rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(26, 61, 52, .035); }
      div[data-testid='stMetricLabel'] { color: #59766e; }
      div[data-testid='stMetricValue'] { color: #174b3d; font-weight: 800; }
      div.stButton > button[kind='primary'], div.stFormSubmitButton > button[kind='primary'] { background: #176858; border: 1px solid #176858; border-radius: 10px; color: white; font-weight: 700; }
      div.stButton > button { border-radius: 10px; }
      [data-testid='stSidebar'] { background: #edf4f1; }
      [data-testid='stSidebar'] h2, [data-testid='stSidebar'] h3 { color: #17483e; }
      .footer { border-top: 1px solid #dce8e3; padding-top: 1rem; color: #61776f; font-size: .82rem; text-align: center; margin-top: 2.5rem; }
      @media (max-width: 640px) { .hero { padding: 1.4rem; border-radius: 16px; } .block-container { padding-left: 1rem; padding-right: 1rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


try:
    records = load_records()
except (OSError, ValueError) as error:
    st.error(f"The demonstration data could not be loaded: {error}")
    st.info("Check that data/plots.json exists and contains valid JSON records.")
    st.stop()

plot_ids = get_unique_plot_ids(records)
flagged_plot_count = sum(
    1 for plot_id in plot_ids
    if get_warnings([record for record in records if record["plot_id"] == plot_id])
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">LandTech 2026 · Problem P5</div>
      <h1>JomiCheck Lite</h1>
      <p>Check before you buy. Explore sample land records, follow ownership history, and spot entries that may need further review — all in one simple dashboard.</p>
      <div class="hero-chip">🌱 Educational prototype · Fictional data only</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Educational prototype using synthetic data. Not an official land-record verification service.",
    icon="⚠️",
)

metric_cols = st.columns(3)
with metric_cols[0]:
    st.metric("Fictional deed records", len(records))
with metric_cols[1]:
    st.metric("Unique plot IDs", len(plot_ids))
with metric_cols[2]:
    st.metric("Plots with demo flags", flagged_plot_count)

st.markdown("<div style='height: .5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-kicker">Start here</div><div class="section-title">Search a plot or deed</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="muted">Enter an exact ID. A deed search also checks other deed records attached to the same plot.</p>',
    unsafe_allow_html=True,
)

if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "last_search" not in st.session_state:
    st.session_state["last_search"] = ""
if "search_now" not in st.session_state:
    st.session_state["search_now"] = False

st.markdown('<div class="sample-label">Or try a prepared scenario</div>', unsafe_allow_html=True)
sample_cols = st.columns(3)
with sample_cols[0]:
    if st.button("✓ Clean example · P-1001", width="stretch", help="A record with no demo rules triggered"):
        st.session_state["search_query"] = "P-1001"
        st.session_state["search_now"] = True
with sample_cols[1]:
    if st.button("! Pending issue · P-1002", width="stretch", help="Mutation is pending in this fictional record"):
        st.session_state["search_query"] = "P-1002"
        st.session_state["search_now"] = True
with sample_cols[2]:
    if st.button("⚑ Deed conflict · P-1018", width="stretch", help="Two fictional records are marked Active for this plot"):
        st.session_state["search_query"] = "P-1018"
        st.session_state["search_now"] = True

with st.form("search_form", clear_on_submit=False):
    query = st.text_input(
        "Plot ID or deed ID",
        key="search_query",
        placeholder="For example: P-1001 or D-2026-1001",
        help="Search uses exact IDs and ignores uppercase/lowercase differences.",
    )
    submitted = st.form_submit_button("Search records", type="primary", width="stretch")

search_requested = submitted or st.session_state.pop("search_now", False)
if search_requested:
    st.session_state["last_search"] = query.strip()

last_search = st.session_state.get("last_search", "")
if last_search:
    matched_records = find_plot_records(records, last_search)
    if not matched_records:
        st.info(
            f"No demo record matched **{last_search}**. Check the ID and try again. "
            "Sample IDs include P-1001, P-1002, P-1018 and D-2026-1001."
        )
    else:
        plot_id = matched_records[0]["plot_id"]
        warnings = get_warnings(matched_records)
        active_records = [
            record for record in matched_records
            if str(record["deed_status"]).casefold() == "active"
        ]
        if len(active_records) > 1:
            owner_summary = "Conflicting entries"
        elif active_records:
            owner_summary = active_records[0]["owner_name"]
        else:
            owner_summary = matched_records[0]["owner_name"]

        # The top summary is intentionally neutral: these are recorded demo fields,
        # not a legal determination about ownership.
        st.markdown("<div style='height: .8rem'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-heading"><div class="section-kicker">Search result</div>'
            f'<div class="section-title">Plot {escape(plot_id)}</div>'
            f'<div class="muted">Showing {len(matched_records)} deed record(s) linked to this plot in the demo data.</div></div>',
            unsafe_allow_html=True,
        )

        current_record = active_records[0] if active_records else matched_records[0]
        detail_cols = st.columns(4)
        with detail_cols[0]:
            st.metric("Recorded owner", owner_summary)
        with detail_cols[1]:
            st.metric("Plot ID", plot_id)
        with detail_cols[2]:
            st.metric("Land area", f"{current_record['area_decimal']:.2f} decimals")
        with detail_cols[3]:
            st.metric("Mutation", current_record["mutation_status"])

        st.markdown("#### Deed details")
        deed_rows = []
        for record in matched_records:
            deed_rows.append({
                "Deed ID": record["deed_id"],
                "Recorded owner": record["owner_name"],
                "Location": record["location"],
                "Registration date": record["registration_date"],
                "Area (decimals)": f"{record['area_decimal']:.2f}",
                "Mutation status": record["mutation_status"],
                "Deed status": record["deed_status"],
                "Acquisition status": record["acquisition_status"],
                "Listed cases": "; ".join(record.get("pending_cases", [])) or "None listed in demo",
            })
        st.dataframe(deed_rows, width="stretch", hide_index=True)

        left_col, right_col = st.columns([1.05, 1])
        with left_col:
            st.markdown("#### Review flags")
            if warnings:
                for warning in warnings:
                    st.warning(f"**{warning['title']}**\n\n{warning['message']}", icon="⚠️")
            else:
                st.success("No flagged issues in demo data", icon="✅")
                st.caption(
                    "This only means the prototype's listed rules did not find a flag. "
                    "It does not prove that a plot is legally clear or fraud-free."
                )
        with right_col:
            st.markdown("#### Case & acquisition summary")
            all_cases = []
            for record in matched_records:
                for case in record.get("pending_cases", []):
                    label = f"{record['deed_id']}: {case}"
                    if label not in all_cases:
                        all_cases.append(label)
            if all_cases:
                for case in all_cases:
                    st.markdown(f"- {case}")
            else:
                st.write("No cases are listed in these fictional records.")
            acquisition_values = sorted({record["acquisition_status"] for record in matched_records})
            st.write("**Acquisition status in the demo:** " + ", ".join(acquisition_values))
            st.caption("Not connected to any government database.")

        st.markdown("#### Ownership history timeline")
        history_events: list[dict[str, str]] = []
        seen_events: set[tuple[str, str, str, str]] = set()
        for record in matched_records:
            for event in record.get("ownership_history", []):
                event_key = (
                    event.get("date", ""), event.get("event", ""),
                    event.get("owner", ""), event.get("deed_id", ""),
                )
                if event_key not in seen_events:
                    seen_events.add(event_key)
                    history_events.append(event)
        history_events.sort(key=lambda event: (event.get("date", ""), event.get("deed_id", "")))

        if history_events:
            with st.container(border=True):
                for index, event in enumerate(history_events):
                    time_col, event_col = st.columns([1, 4])
                    with time_col:
                        st.markdown(f"<div class='timeline-date'>{escape(event.get('date', 'Date unknown'))}</div>", unsafe_allow_html=True)
                        if index < len(history_events) - 1:
                            st.caption("│")
                    with event_col:
                        st.markdown(f"<div class='timeline-owner'>{escape(event.get('owner', 'Unknown owner'))}</div>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div class='timeline-event'>{escape(event.get('event', 'Record event'))} · "
                            f"Deed {escape(event.get('deed_id', 'Unknown'))}</div>",
                            unsafe_allow_html=True,
                        )
                    if index < len(history_events) - 1:
                        st.markdown("<div style='border-bottom:1px solid #e7efeb; margin:.35rem 0 .7rem 0'></div>", unsafe_allow_html=True)
        else:
            st.info("No ownership history is included for this demo record.")

        with st.expander("How are review flags calculated?"):
            st.markdown(
                "- **Multiple active deeds:** more than one record for the same plot is marked Active.\n"
                "- **Mutation not completed:** a deed's mutation status is not Completed.\n"
                "- **Listed case or dispute:** a record has one or more case descriptions in the sample data.\n"
                "- **Acquisition status:** the record says something other than Clear.\n"
                "- **Deed not active:** a record is marked Transferred, Revoked or another non-Active status.\n\n"
                "These are simple, inspectable rules over fictional JSON data. They are not proof of fraud, title, ownership, or legal status."
            )
else:
    st.markdown(
        """
        <div style="background:#ffffff;border:1px solid #e1ebe7;border-radius:16px;padding:1.1rem 1.25rem;margin-top:1rem;">
          <div style="font-weight:800;color:#1a4c40;margin-bottom:.3rem;">Ready to explore?</div>
          <div style="color:#607770;line-height:1.6;">Choose one of the sample scenarios above, or enter a plot/deed ID. The clean example, pending-mutation example and conflicting-deeds example are prepared for your demo presentation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.markdown("## 🌱 JomiCheck Lite")
    st.caption("LandTech 2026 · P5: Citizen Pre-Purchase Verification")
    st.markdown("---")
    st.markdown("### Demo scenarios")
    st.markdown("**P-1001**  \nNo review flags in sample rules")
    st.markdown("**P-1002**  \nMutation marked Pending")
    st.markdown("**P-1018**  \nTwo Active deed entries")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Enter an exact plot ID or deed ID.\n2. Review the recorded fields.\n3. Read each warning's reason.\n4. Check the chronological history.")
    st.markdown("---")
    st.caption("All names, IDs, case notes and locations are fictional and for demonstration only.")

st.markdown(
    '<div class="footer">JomiCheck Lite · Educational prototype using synthetic data · Not an official land-record verification service</div>',
    unsafe_allow_html=True,
)
