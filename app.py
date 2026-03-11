import streamlit as st
from modules.components.sidebar import sidebar
from modules.sheets_client import get_data_worksheet

import streamlit as st
import pandas as pd

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈")
st.title("📈 Dashboard Data Collection Jatim Barat")
sidebar()

df_database = get_data_worksheet()


from utils.selector import pilih_segmen
from modules.metrics import compute_metrics

segmen_target = pilih_segmen()

df_database["billper"] = pd.to_datetime(
    df_database["billper"],
    format="%d/%m/%Y"
).dt.date

df_database, metrics = compute_metrics(df_database, segmen_target)
col1, col2 = st.columns(2)

col2.metric(
    "Saldo Hari Ini (dibanding kemarin)",
    f"{metrics['today']:,.0f}",
    f"{metrics['delta_yesterday']:,.0f}",
    delta_color="inverse"
)

col1.metric(
    "Saldo Awal Bulan Ini",
    f"{metrics['day6']:,.0f}",
    f"{metrics['delta_day6']:,.0f}",
    delta_color="inverse"
)

st.dataframe(df_database)