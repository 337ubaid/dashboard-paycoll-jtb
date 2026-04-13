import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.constant import HARI_LIBUR
from services.chart import get_available_billperiodes, prepare_forecast_nonpots
from services.filters import filter_collection_data
from utils.formatter import format_skala_rupiah


def print_chart_tren_saldo(df_nonpots, segmen_target):
    st.subheader("Tren Saldo")

    # Billperiode selector
    available_bps = get_available_billperiodes(df_nonpots)

    # Format billperiodes for display
    bp_options = ["Semua Periode"] + [
        f"{bp // 100}-{bp % 100:02d}" for bp in available_bps
    ]
    selected_bp_display = st.selectbox(
        "Pilih Bill Periode", bp_options, index=len(bp_options) - 1
    )

    # Convert back to integer or None
    if selected_bp_display == "Semua Periode":
        selected_billperiode = None
    else:
        bp_parts = selected_bp_display.split("-")
        selected_billperiode = int(bp_parts[0]) * 100 + int(bp_parts[1])

    # Filter for chart
    df_filtered = filter_collection_data(df_nonpots, segmen_target)

    # Prepare chart data
    df_chart = prepare_forecast_nonpots(df_filtered, billperiode=selected_billperiode)

    # Determine mode
    chart_mode = "daily" if selected_billperiode else "billperiode"

    plot_chart(df_chart, mode=chart_mode)


def plot_chart(df, mode="billperiode", value_col="saldo_akhir"):
    """
    Plot chart with support for both billperiode and daily modes.

    Args:
        df: DataFrame from prepare_forecast_nonpots
        mode: "billperiode" (aggregated by period) or "daily" (daily progression)
        value_col: Value column to plot
    """
    fig = go.Figure()

    if df.empty:
        st.warning("Tidak ada data untuk ditampilkan")
        return

    # ======================
    # 1. LINE PLOT
    # ======================

    for t, style in [("actual", "solid"), ("forecast", "dash")]:
        d = df[df["type"] == t]

        if d.empty:
            continue

        if mode == "daily":
            x_col = "date"
        else:
            x_col = "billperiode"

        fig.add_trace(
            go.Scatter(
                x=d[x_col],
                y=d[value_col],
                mode="lines+markers",
                name=t,
                line=dict(dash=style),
            )
        )

    # ======================
    # 2. LAST POINT LABEL
    # ======================

    if mode == "daily":
        x_col = "date"
    else:
        x_col = "billperiode"

    last = df.sort_values(x_col).groupby("type").tail(1)

    for _, r in last.iterrows():
        x_val = r[x_col]
        fig.add_trace(
            go.Scatter(
                x=[x_val],
                y=[r[value_col]],
                mode="text",
                text=[f"{format_skala_rupiah(r[value_col])}"],
                showlegend=False,
                textposition="top right",
                textfont=dict(size=14),
            )
        )

    # ======================
    # 3. AXIS CONTROL
    # ======================

    max_val = df[value_col].max()
    fig.update_yaxes(range=[0, max_val * 1.1])

    if mode == "daily":
        fig.update_xaxes(
            range=[df["date"].min(), df["date"].max() + pd.Timedelta(days=3)]
        )
    else:
        fig.update_xaxes(type="category")

    fig.update_layout(hovermode="x unified", margin=dict(t=25, b=0, l=0, r=0))

    # ======================
    # 4. LIBUR AREA (only for daily mode)
    # ======================
    if mode == "daily":
        libur_ranges = HARI_LIBUR

        for start, end, label in libur_ranges:
            fig.add_vrect(
                x0=start,
                x1=end,
                fillcolor="gray",
                opacity=0.1,
                line_width=0,
                annotation_text=label,
                annotation_position="top left",
            )

    st.plotly_chart(fig, width="stretch")


def add_weekly_lines(fig, df, date_col):
    start = df[date_col].min()
    end = df[date_col].max()

    for d in pd.date_range(start=start, end=end, freq="W-MON"):
        fig.add_vline(
            x=d,
            line=dict(
                dash="dot",
                width=1,
            ),
        )
