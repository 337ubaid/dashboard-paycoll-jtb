import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.constant import HARI_LIBUR
from utils.formatter import format_skala_rupiah


def plot_chart(df, date_col="tanggal", value_col="saldo_akhir"):

    fig = go.Figure()

    # ======================
    # 1. LINE PLOT
    # ======================

    for t, style in [("actual", "solid"), ("forecast", "dash")]:
        d = df[df["type"] == t]

        fig.add_trace(
            go.Scatter(
                x=d[date_col],
                y=d[value_col],
                mode="lines+markers",
                name=t,
                line=dict(dash=style),
            )
        )

    # ======================
    # 2. LAST POINT LABEL
    # ======================

    last = df.sort_values(date_col).groupby("type").tail(1)

    for _, r in last.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[r[date_col]],
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
    fig.update_xaxes(
        range=[df[date_col].min(), df[date_col].max() + pd.Timedelta(days=3)]
    )

    fig.update_layout(hovermode="x unified", margin=dict(t=25, b=0, l=0, r=0))

    # ======================
    # 4. LIBUR AREA
    # ======================
    # Tambahkan Libur
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

    st.plotly_chart(fig, use_container_width=True)
