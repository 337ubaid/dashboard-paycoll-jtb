import streamlit as st

from data.database import load_database_nonpots
from services.chart import prepare_total_with_forecast
from services.filters import filter_collection_data
from ui.chart import plot_chart
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

# METRIC
render_dashboard_metrics(df_nonpots, segmen_target)

# Grafik
st.subheader("Tren Saldo Harian")
c1, c2 = st.columns(2)
with c1:
    df_chart = prepare_total_with_forecast(
        filter_collection_data(df_nonpots, segmen_target)
    )

    plot_chart(df_chart)
# SHOW ALL DATA
df_nonpots = filter_collection_data(df_nonpots, segmen_target, tanggal=LATEST_DATE)
print_sort_dataframe(df_nonpots)
