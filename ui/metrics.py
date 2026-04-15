import streamlit as st

from services.metrics_service import calculate_dashboard_metrics


def render_dashboard_metrics(df, segmen="-Semua-"):
    st.subheader("Metric Saldo")

    df, saldo, pelanggan, different_days, latest_date = calculate_dashboard_metrics(
        df, segmen
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Saldo Awal Bulan Ini",
            f"{saldo['start_periode']:,.0f}",
            f"{saldo['delta_start_periode']:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            f"Saldo Hari Ini (dibanding {different_days} hari lalu)",
            f"{saldo['today']:,.0f}",
            f"{saldo['delta_yesterday']:,.0f}",
            delta_color="inverse",
        )

    with col2:

        st.metric(
            "Pelanggan Awal Bulan Ini",
            f"{pelanggan['start_periode']:,.0f}",
            f"{pelanggan['delta_start_periode']:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            f"Pelanggan Hari Ini (dibanding  {different_days} hari lalu)",
            f"{pelanggan['today']:,.0f}",
            f"{pelanggan['delta_yesterday']:,.0f}",
            delta_color="inverse",
        )

    st.info(f"Terakhir diperbarui **{latest_date}**")
