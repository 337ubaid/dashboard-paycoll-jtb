import streamlit as st
from ui.layout import (
    render_sidebar,
    render_dataframe,
    print_sort_dataframe,
    render_all_kuadran,
)
from data.database import load_database_nonpots
from services.filters import filter_collection_data
from ui.metrics import render_dashboard_metrics
from datetime import date
from core.constant import COLUMNS_TUNGGAKAN_AM, COLUMNS_KUADRAN
from services.kuadran_service import prepare_kuadran_data
from utils.selector import pilih_segmen, cari_am


TODAY = date.today()
render_sidebar()
df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Tunggakan AM")
# ==============================

# FILTERING
segmen_target = pilih_segmen()
filtered_df = cari_am(df_database)

# METRICS
render_dashboard_metrics(filtered_df)

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
        print_sort_dataframe(filtered_df[filtered_df["kuadran"] == i])
