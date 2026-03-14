import streamlit as st
from data.database import load_database_nonpots
from ui.layout import render_sidebar, render_dataframe
from ui.metrics import render_dashboard_metrics
from utils.selector import pilih_segmen
from services.filters import filter_collection_data
from core.constant import TODAY

render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Dashboard Data Collection Jatim Barat")

df_nonpots = load_database_nonpots()

segmen_target = pilih_segmen()

# METRIC
render_dashboard_metrics(df_nonpots, segmen_target)
# SHOW ALL DATA
latest_date = df_nonpots["tanggal"].max()  # FIX -> globally accessible
df_nonpots = filter_collection_data(df_nonpots, segmen_target, tanggal=latest_date)
render_dataframe(df_nonpots)
