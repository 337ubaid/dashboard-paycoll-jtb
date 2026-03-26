import streamlit as st
from data.database import load_database_nonpots
from ui.layout import render_sidebar, print_sort_dataframe
from ui.metrics import render_dashboard_metrics
from utils.selector import pilih_segmen
from services.filters import filter_collection_data
from core.constant import TODAY

render_sidebar()
df_nonpots = load_database_nonpots()
LATEST_DATE = df_nonpots["tanggal"].max()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Dashboard Data Collection Jatim Barat")
# ==============================

segmen_target = pilih_segmen()

# METRIC
render_dashboard_metrics(df_nonpots, segmen_target)
# SHOW ALL DATA
df_nonpots = filter_collection_data(df_nonpots, segmen_target, tanggal=LATEST_DATE)
print_sort_dataframe(df_nonpots)
