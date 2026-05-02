import streamlit as st
import pandas as pd

from simulation import run_simulation
from charts import chart_delivery_hist, chart_driver_util, chart_queue_length
from exports import export_orders_excel
from ui import load_css, show_hero, show_pipeline, show_kpi_cards, show_section

st.set_page_config(layout="wide", page_title="DeliverSim")

load_css()
show_hero()
show_pipeline()

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
    "<div class='sidebar-label'><i class='fa-solid fa-gear' style='color: rgb(128,128,128);'></i> Simulation Config</div>",
    unsafe_allow_html=True
)
    sim_time = st.slider("Simulation Time (min)", 60, 600, 240)
    drivers = st.slider("Drivers", 1, 20, 5)
    restaurants = st.slider("Restaurants", 1, 10, 3)

    st.markdown(
    "<div class='sidebar-label' style='margin-top:18px'>"
    "<i class='fa-solid fa-kitchen-set' style='color: rgb(128,128,128);'></i> Kitchen Settings"
    "</div>",
    unsafe_allow_html=True
)
    prep_mean = st.slider("Avg Prep Time (min)", 2, 20, 8)
    prep_std = st.slider("Prep Time Variation", 0, 8, 2)

    st.markdown(
    "<div class='sidebar-label' style='margin-top:18px'>"
    "<i class='fa-solid fa-truck-moving' style='color: rgb(128,128,128);'></i> Settings"
    "</div>",
    unsafe_allow_html=True
)
    travel_mean = st.slider("Avg Travel Time (min)", 5, 40, 15)
    travel_std = st.slider("Travel Time Variation", 0, 10, 4)
    arrival_rate = st.slider("Order Arrival Rate", 0.1, 3.0, 0.8, step=0.1,
                              help="Orders per minute on average")
    delay_threshold = st.slider("Delay Threshold (min)", 20, 90, 45,
                                 help="Orders exceeding this are marked as delayed")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("▶ Run Simulation")

# ── Run ──────────────────────────────────────────────────
if run_btn:
    with st.spinner("Running simulation..."):
        results = run_simulation(
            sim_time=sim_time,
            num_restaurants=restaurants,
            num_drivers=drivers,
            arrival_rate=arrival_rate,
            prep_time_mean=prep_mean,
            prep_time_std=prep_std,
            travel_time_mean=travel_mean,
            travel_time_std=travel_std,
            delay_threshold=delay_threshold
        )
  # ── Orders Table ─────────────────────────────────────
    show_section("Order Log", "📋")
    df = pd.DataFrame(results.order_log)

    # Color incomplete rows visually with a note
    completed_df = df[df["Status"] == "Completed"]
    incomplete_df = df[df["Status"] != "Completed"]

    st.dataframe(df, use_container_width=True)

    if results.incomplete_orders > 0:
        st.markdown(f"""
        <div class='info-box'>
            ⚠️ <strong>{results.incomplete_orders} incomplete orders</strong> were still in-progress when the simulation ended.
            These are shown at the bottom of the table with their last known stage.
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Cards ────────────────────────────────────────
    show_kpi_cards(results)

    # ── Charts ───────────────────────────────────────────
    show_section("Analytics", "📊")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(chart_delivery_hist(results, delay_threshold), use_container_width=True)
    with col2:
        st.plotly_chart(chart_driver_util(results), use_container_width=True)

    st.plotly_chart(chart_queue_length(results), use_container_width=True)

  
    # ── Download ─────────────────────────────────────────
    show_section("Export", "💾")
    file = export_orders_excel(results)
    st.download_button(
        "⬇ Download Excel Report",
        file,
        "DeliverSim_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
