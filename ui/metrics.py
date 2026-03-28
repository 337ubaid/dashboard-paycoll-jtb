import streamlit as st

from services.metrics_service import calculate_dashboard_metrics


def render_dashboard_metrics(df, segmen="-Semua-"):

    df, saldo, pelanggan = calculate_dashboard_metrics(df, segmen)

    latest_date = df["tanggal"].max()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Saldo Awal Bulan Ini",
            f"{saldo['day6']:,.0f}",
            f"{saldo['delta_day6']:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            "Saldo Hari Ini (dibanding 3 hari lalu)",
            f"{saldo['today']:,.0f}",
            f"{saldo['delta_yesterday']:,.0f}",
            delta_color="inverse",
        )

    with col2:

        st.metric(
            "Pelanggan Awal Bulan Ini",
            f"{pelanggan['day6']:,.0f}",
            f"{pelanggan['delta_day6']:,.0f}",
            delta_color="inverse",
        )

        st.metric(
            "Pelanggan Hari Ini (dibanding 3 hari lalu)",
            f"{pelanggan['today']:,.0f}",
            f"{pelanggan['delta_yesterday']:,.0f}",
            delta_color="inverse",
        )

    st.info(f"Terakhir diperbarui **{latest_date}**")
