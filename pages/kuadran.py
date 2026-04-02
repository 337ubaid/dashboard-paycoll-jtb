from datetime import date

import streamlit as st

from core.constant import COLUMNS_KUADRAN, COLUMNS_TUNGGAKAN_AM
from data.database import load_database_nonpots
from services.chart import prepare_total_with_forecast
from services.filters import filter_collection_data
from services.kuadran_service import prepare_kuadran_data
from ui.chart import plot_chart
from ui.layout import (
    print_sort_dataframe,
    render_all_kuadran,
    render_dataframe,
    render_sidebar,
)
from ui.metrics import render_dashboard_metrics
from utils.selector import cari_am, pilih_all_segmen

TODAY = date.today()
render_sidebar()
df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Kuadran")
# ==============================

# FILTERING
segmen_target = pilih_all_segmen()
filtered_df = cari_am(df_database)

c1, c2 = st.columns(2)
# METRICS
with c1:
    render_dashboard_metrics(filtered_df, segmen_target)
with c2:
    df_chart = prepare_total_with_forecast(
        filter_collection_data(filtered_df, segmen_target)
    )

    plot_chart(df_chart)

# KUADRAN & SUMMARY
tab_kuadran, tab_summary = st.tabs(["Kuadran", "Summary"])
filtered_df = filter_collection_data(filtered_df, segmen_target, tanggal=latest_date)


with tab_kuadran:
    df_kuadran, total_pelanggan, total_saldo = prepare_kuadran_data(
        filtered_df, segmen_target, COLUMNS_KUADRAN
    )

    render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)
with tab_summary:
    print_sort_dataframe(filtered_df[COLUMNS_TUNGGAKAN_AM])

# DETAIL KUADRAN
st.divider()
st.subheader("Detail Kuadran")

tab_names = ["Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs, start=1):
    with tab:
        df_kuadran = filtered_df[filtered_df["kuadran"] == i]
        st.info(f"{len(df_kuadran)} Pelanggan")
        print_sort_dataframe(df_kuadran)
