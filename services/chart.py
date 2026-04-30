from datetime import date, timedelta
from typing import Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.constant import HARI_LIBUR
from utils.formatter import format_skala_rupiah


def plot_chart(df: pd.DataFrame, mode: str = "billperiode", value_col: str = "saldo_akhir"):
    """
    Plot chart with support for both billperiode and daily modes.

    Args:
        df: DataFrame from prepare_forecast_nonpots
        mode: "billperiode" (aggregated by period) or "daily" (daily progression)
        value_col: Value column to plot
    """
    if df.empty:
        return

    fig = go.Figure()
    x_col = "date" if mode == "daily" else "billperiode"

    # ======================
    # 1. LINE PLOT
    # ======================
    for t, style in [("actual", "solid"), ("forecast", "dash")]:
        d = df[df["type"] == t]
        if d.empty:
            continue

        fig.add_trace(
            go.Scatter(
                x=d[x_col],
                y=d[value_col],
                mode="lines+markers",
                name=t.capitalize(),
                line=dict(dash=style),
            )
        )

    # ======================
    # 2. LAST POINT LABEL
    # ======================
    last = df.sort_values(x_col).groupby("type").tail(1)
    for _, r in last.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[r[x_col]],
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

    fig.update_layout(
        hovermode="x unified",
        margin=dict(t=25, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # ======================
    # 4. LIBUR AREA (only for daily mode)
    # ======================
    if mode == "daily":
        for start, end, label in HARI_LIBUR:
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


def get_available_billperiodes(df: pd.DataFrame) -> list:
    """Get sorted list of available billperiodes from dataframe."""
    if "billperiode" in df.columns:
        billperiodes = df["billperiode"].dropna().unique()
        return sorted(billperiodes)
    return []


def prepare_forecast_nonpots(df: pd.DataFrame, billperiode: Optional[int] = None, value_col: str = "saldo_akhir") -> pd.DataFrame:
    """
    Prepare forecast data grouped by billperiode or daily within a specific billperiode.
    """
    if billperiode is not None:
        return _prepare_daily_forecast(df, billperiode, value_col)
    return _prepare_period_forecast(df, value_col)


def _prepare_daily_forecast(df: pd.DataFrame, billperiode: int, value_col: str) -> pd.DataFrame:
    """Internal helper for daily progression forecast."""
    df_filtered = df[df["billperiode"] == billperiode].copy()
    if df_filtered.empty:
        return pd.DataFrame()

    df_filtered["tanggal_dt"] = pd.to_datetime(df_filtered["tanggal"], errors="coerce")
    df_actual = (
        df_filtered.groupby("tanggal_dt")[value_col]
        .sum()
        .reset_index()
        .sort_values("tanggal_dt")
    )
    df_actual.rename(columns={"tanggal_dt": "date"}, inplace=True)

    trend = df_actual[value_col].diff().tail(7).mean() if len(df_actual) > 1 else 0
    last_date = df_actual["date"].max()
    last_value = df_actual[value_col].iloc[-1]

    # Determine end of period (day 5 of next month)
    year, month = divmod(billperiode, 100)
    if month == 12:
        end_period = date(year + 1, 1, 5)
    else:
        end_period = date(year, month + 1, 5)

    future_dates = pd.date_range(last_date + timedelta(days=1), end_period, freq="D")
    vals = [last_value + (trend * (i + 1)) for i in range(len(future_dates))]

    df_forecast = pd.DataFrame({
        "date": future_dates,
        value_col: vals if vals else [last_value]
    })

    df_actual["type"] = "actual"
    df_forecast["type"] = "forecast"

    return pd.concat([df_actual, df_forecast])


def _prepare_period_forecast(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Internal helper for period-to-period forecast."""
    df_actual = (
        df.groupby("billperiode")[value_col]
        .sum()
        .reset_index()
        .sort_values("billperiode")
    )
    if df_actual.empty:
        return pd.DataFrame()

    trend = df_actual[value_col].diff().tail(3).mean()
    last_bp = df_actual["billperiode"].max()
    last_value = df_actual[value_col].iloc[-1]

    year, month = divmod(last_bp, 100)
    next_bp = (year + 1) * 100 + 1 if month == 12 else year * 100 + month + 1

    df_forecast = pd.DataFrame({
        "billperiode": [next_bp],
        value_col: [last_value + trend]
    })

    df_actual["type"] = "actual"
    df_forecast["type"] = "forecast"

    return pd.concat([df_actual, df_forecast])
