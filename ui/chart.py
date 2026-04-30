import pandas as pd
import streamlit as st

from services.chart import (
    get_available_billperiodes,
    plot_chart,
    prepare_forecast_nonpots,
)

from data.supabase import get_chart_data_nonpots


def print_chart_tren_saldo(filters):
    st.subheader("Tren Saldo")

    # Fetch data
    df_filtered = get_chart_data_nonpots(filters)

    # Billperiode selector
    available_bps = get_available_billperiodes(df_filtered)

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

    # Prepare chart data
    df_chart = prepare_forecast_nonpots(df_filtered, billperiode=selected_billperiode)

    # Determine mode
    chart_mode = "daily" if selected_billperiode else "billperiode"

    plot_chart(df_chart, mode=chart_mode)


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


def get_previous_billperiode(billperiode):
    month = billperiode % 100
    year = billperiode // 100

    if month == 1:
        return (year - 1) * 100 + 12  # Year changes from 2026 to 2025, month = 12
    else:
        return year * 100 + (month - 1)
