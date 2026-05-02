import streamlit as st
import numpy as np

def load_css():
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def show_hero():
    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>▸ DISCRETE EVENT SIMULATION</div>
<h1 class='hero-title'>
    Deliv<span style="color: #f97316;">RO</span>
    <i class="fa-solid fa-truck-arrow-right" style="color: rgb(255, 4, 4); padding-left:10px;"></i>
</h1>
    <p class='hero-sub'>Food Delivery Operations Simulator — Model queues, bottlenecks, and driver efficiency in real time.</p>
    </div>
    """, unsafe_allow_html=True)

def show_pipeline():
    st.markdown("""
    <div class='pipeline'>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-cart-shopping" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>Order<br>Placed</div>
        </div>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-clock" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>Prep<br>Queue</div>
        </div>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-utensils" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>Cooking</div>
        </div>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-clock" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>Driver<br>Queue</div>
        </div>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-gauge-high" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>En Route</div>
        </div>
        <div class='pipe-step'>
            <div class='pipe-icon active'><i class="fa-solid fa-box-open" style="color: rgb(255, 212, 59);"></i></div>
            <div class='pipe-label'>Delivered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_kpi_cards(results):
    completed = results.completed_orders
    delayed = results.delayed_orders
    avg_time = round(np.mean(results.delivery_times), 1) if results.delivery_times else 0
    delay_rate = round((delayed / completed * 100), 1) if completed > 0 else 0
    avg_util = round(np.mean([x[1] for x in results.driver_util_log]), 1) if results.driver_util_log else 0

    st.markdown(f"""
    <div class='metric-grid'>
        <div class='metric-card orange'>
            <div class='accent-line'></div>
            <div class='metric-label'>Total Orders</div>
            <div class='metric-value'>{results.total_orders}</div>
            <div class='metric-unit'>{completed} completed · {results.incomplete_orders} incomplete</div>
        </div>
        <div class='metric-card teal'>
            <div class='accent-line'></div>
            <div class='metric-label'>Avg Delivery Time</div>
            <div class='metric-value'>{avg_time}</div>
            <div class='metric-unit'>minutes per order</div>
        </div>
        <div class='metric-card rose'>
            <div class='accent-line'></div>
            <div class='metric-label'>Delay Rate</div>
            <div class='metric-value'>{delay_rate}%</div>
            <div class='metric-unit'>{delayed} orders exceeded threshold</div>
        </div>
        <div class='metric-card violet'>
            <div class='accent-line'></div>
            <div class='metric-label'>Driver Utilization</div>
            <div class='metric-value'>{avg_util}%</div>
            <div class='metric-unit'>average across simulation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_section(title, icon=""):
    st.markdown(f"""
    <div class='section-header'>{icon} {title}</div>
    """, unsafe_allow_html=True)
