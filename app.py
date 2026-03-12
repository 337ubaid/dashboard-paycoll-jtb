import streamlit as st
from modules.components.sidebar import sidebar
from modules.sheets_client import load_database
from utils.validator import format_currency
import streamlit as st
import pandas as pd
from utils.selector import pilih_segmen
from modules.metrics import compute_metrics

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈")
st.title("📈 Dashboard Data Collection Jatim Barat")
sidebar()

df_database = load_database()

segmen_target = pilih_segmen()



# METRIC
df_database, metrics_saldo, metrics_pelanggan = compute_metrics(df_database, segmen_target)
col1, col2 = st.columns(2)
with col1:
    ## METRIC SALDO AWAL
    st.metric(
        "Saldo Awal Bulan Ini",
        f"{metrics_saldo['day6']:,.0f}",
        f"{metrics_saldo['delta_day6']:,.0f}",
        delta_color="inverse"
    )
    ## METRIC SALDO TODAY
    st.metric(
        "Saldo Hari Ini (dibanding 3 hari lalu)",
        f"{metrics_saldo['today']:,.0f}",
        f"{metrics_saldo['delta_yesterday']:,.0f}",
        delta_color="inverse"
    )
with col2:
    st.metric(
        "Pelanggan Awal Bulan Ini",
        f"{metrics_pelanggan['day6']:,.0f}",
        f"{metrics_pelanggan['delta_day6']:,.0f}",
        delta_color="inverse"
    )
    st.metric(
        "Pelanggan Hari Ini (dibanding 3 hari lalu)",
        f"{metrics_pelanggan['today']:,.0f}",
        f"{metrics_pelanggan['delta_yesterday']:,.0f}",
        delta_color="inverse"
    )
# SHOW ALL DATA
st.dataframe(format_currency(df_database))