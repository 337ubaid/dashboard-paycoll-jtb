from typing import Optional

import pandas as pd
import streamlit as st

from data.supabase import get_chart_data_nonpots
from services.chart import (
    get_available_billperiodes,
    plot_chart,
    prepare_forecast_nonpots,
)
from services.filters import filter_collection_data


def render_trend_chart(df: Optional[pd.DataFrame] = None, filters: Optional[dict] = None, segmen_target: str = "-Semua-"):
    """
    Unified function to render trend chart.
    If df is provided, it uses it and filters by segmen_target.
    If filters is provided, it fetches data from Supabase.
    """
    st.subheader("Tren Saldo")

    # 1. Fetch or use provided data
    if df is None:
        if filters is None:
            filters = {}
        df_filtered = get_chart_data_nonpots(filters)
    else:
        df_filtered = filter_collection_data(df, segmen_target)

    if df_filtered.empty:
        st.warning("Tidak ada data untuk ditampilkan")
        return

    # 2. Billperiode selection UI
    available_bps = get_available_billperiodes(df_filtered)
    bp_options = ["Semua Periode"] + [f"{bp // 100}-{bp % 100:02d}" for bp in available_bps]
    
    selected_bp_display = st.selectbox(
        "Pilih Bill Periode", 
        bp_options, 
        index=len(bp_options) - 1,
        key="bp_selector"
    )

    # 3. Process selection
    selected_billperiode = None
    if selected_bp_display != "Semua Periode":
        bp_parts = selected_bp_display.split("-")
        selected_billperiode = int(bp_parts[0]) * 100 + int(bp_parts[1])

    # 4. Prepare and plot
    df_chart = prepare_forecast_nonpots(df_filtered, billperiode=selected_billperiode)
    chart_mode = "daily" if selected_billperiode else "billperiode"
    plot_chart(df_chart, mode=chart_mode)


def print_chart_tren_saldo_supabase(filters):
    """Legacy wrapper for Supabase trend chart."""
    render_trend_chart(filters=filters)


def print_chart_tren_saldo(df_nonpots, segmen_target):
    """Legacy wrapper for local trend chart."""
    render_trend_chart(df=df_nonpots, segmen_target=segmen_target)


def add_weekly_lines(fig, df, date_col):
    """Helper to add weekly vertical lines to a Plotly figure."""
    start = df[date_col].min()
    end = df[date_col].max()

    for d in pd.date_range(start=start, end=end, freq="W-MON"):
        fig.add_vline(
            x=d,
            line=dict(dash="dot", width=1),
        )


def get_previous_billperiode(billperiode: int) -> int:
    """Calculate the previous billperiode integer (YYYYMM)."""
    year, month = divmod(billperiode, 100)
    if month == 1:
        return (year - 1) * 100 + 12
    return year * 100 + (month - 1)
