import plotly.graph_objects as go
import plotly.express as px
import numpy as np

DARK_BG = "#0d0f14"
CARD_BG = "#13161f"
GRID_COLOR = "#1f2840"
TEXT_COLOR = "#94a3b8"
ORANGE = "#f97316"
VIOLET = "#a78bfa"
TEAL = "#2dd4bf"
ROSE = "#fb7185"

BASE_LAYOUT = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(family="Sora, sans-serif", color=TEXT_COLOR, size=12),
    margin=dict(l=20, r=20, t=50, b=20),

)


def chart_delivery_hist(results, delay_threshold):
    times = results.delivery_times

    on_time = [t for t in times if t <= delay_threshold]
    delayed = [t for t in times if t > delay_threshold]

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=on_time,
        nbinsx=20,
        name="On Time",
        marker_color=TEAL,
        opacity=0.85,
    ))

    fig.add_trace(go.Histogram(
        x=delayed,
        nbinsx=20,
        name="Delayed",
        marker_color=ROSE,
        opacity=0.85,
    ))

    fig.add_vline(
        x=delay_threshold,
        line_dash="dash",
        line_color=ORANGE,
        line_width=2,
        annotation_text=f"Threshold ({delay_threshold} min)",
        annotation_font_color=ORANGE,
        annotation_position="top right"
    )

    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text="Delivery Time Distribution", font=dict(color="#f1f5f9", size=14)),
        barmode="overlay",
        xaxis_title="Minutes",
        yaxis_title="Orders",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )

    return fig


def chart_driver_util(results):
    times = [x[0] for x in results.driver_util_log]
    util = [x[1] for x in results.driver_util_log]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=times,
        y=util,
        mode="lines",
        name="Utilization %",
        line=dict(color=VIOLET, width=2),
        fill="tozeroy",
        fillcolor="rgba(124,58,237,0.08)",
    ))

    fig.add_hline(
        y=80,
        line_dash="dot",
        line_color=ORANGE,
        line_width=1.5,
        annotation_text="80% threshold",
        annotation_font_color=ORANGE,
        annotation_position="bottom right"
    )

    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text="Driver Utilization Over Time", font=dict(color="#f1f5f9", size=14)),
        xaxis_title="Simulation Time (min)",
        yaxis_title="Utilization %",
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, range=[0, 105]),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
    )

    return fig


def chart_queue_length(results):
    times = [x[0] for x in results.queue_log]
    rest_q = [x[1] for x in results.queue_log]
    driver_q = [x[2] for x in results.queue_log]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=times,
        y=rest_q,
        mode="lines",
        name="Restaurant Queue",
        line=dict(color=ORANGE, width=2),
        fill="tozeroy",
        fillcolor="rgba(249,115,22,0.07)",
    ))

    fig.add_trace(go.Scatter(
        x=times,
        y=driver_q,
        mode="lines",
        name="Driver Queue",
        line=dict(color=TEAL, width=2),
        fill="tozeroy",
        fillcolor="rgba(45,212,191,0.07)",
    ))

    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text="Queue Lengths Over Time", font=dict(color="#f1f5f9", size=14)),
        xaxis_title="Simulation Time (min)",
        yaxis_title="Orders Waiting",
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
    )

    return fig
