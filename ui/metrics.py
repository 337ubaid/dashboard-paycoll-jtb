import streamlit as st

from services.metrics_service import (
    calculate_dashboard_metrics,
    calculate_dashboard_metrics_supabase,
    DashboardMetrics,
)


def render_dashboard_metrics(df, segmen="-Semua-"):
    """Render dashboard metrics from raw dataframe."""
    _, metrics = calculate_dashboard_metrics(df, segmen)
    _render_metrics_ui(metrics)


def render_dashboard_metrics_supabase(data_metric):
    """Render dashboard metrics from Supabase summary data."""
    metrics = calculate_dashboard_metrics_supabase(data_metric)
    _render_metrics_ui(metrics)


def _render_metrics_ui(metrics: DashboardMetrics):
    """Unified UI rendering for dashboard metrics."""
    st.subheader("Metric Saldo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Saldo Awal Bulan Ini",
            f"{metrics.saldo.start_periode:,.0f}",
            f"{metrics.saldo.delta_start_periode:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            f"Saldo Hari Ini (dibanding {metrics.different_days} hari lalu)",
            f"{metrics.saldo.today:,.0f}",
            f"{metrics.saldo.delta_yesterday:,.0f}",
            delta_color="inverse",
        )

    with col2:
        st.metric(
            "Pelanggan Awal Bulan Ini",
            f"{metrics.pelanggan.start_periode:,.0f}",
            f"{metrics.pelanggan.delta_start_periode:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            f"Pelanggan Hari Ini (dibanding {metrics.different_days} hari lalu)",
            f"{metrics.pelanggan.today:,.0f}",
            f"{metrics.pelanggan.delta_yesterday:,.0f}",
            delta_color="inverse",
        )

    if metrics.latest_date:
        st.info(f"Terakhir diperbarui **{metrics.latest_date}**")
