import streamlit as st

from data.database import load_database_nonpots
from services.filters import filter_collection_data
from ui.chart import print_chart_tren_saldo
from ui.layout import print_sort_dataframe, render_sidebar
from ui.metrics import render_dashboard_metrics
from utils.selector import pilih_all_segmen

render_sidebar()
df_nonpots = load_database_nonpots()
LATEST_DATE = df_nonpots["tanggal"].max()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Dashboard Data Collection Jatim Barat")
# ==============================

segmen_target = pilih_all_segmen()
if segmen_target is None:
    segmen_target = "-Semua-"

c1, c2 = st.columns(2)
with c1:
    # METRIC
    render_dashboard_metrics(df_nonpots, segmen_target)
with c2:
    # Grafik
    print_chart_tren_saldo(df_nonpots, segmen_target)

# SHOW ALL DATA
df_nonpots = filter_collection_data(df_nonpots, segmen_target, tanggal=LATEST_DATE)
print_sort_dataframe(df_nonpots)
