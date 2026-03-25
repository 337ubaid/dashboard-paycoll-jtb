import streamlit as st
from ui.layout import (
    render_sidebar,
    render_dataframe,
    print_dataframe,
    render_all_kuadran,
)
from data.database import load_database_nonpots
from services.filters import filter_collection_data
from ui.metrics import render_dashboard_metrics
from datetime import date
from core.constant import COLUMNS_TUNGGAKAN_AM, COLUMNS_KUADRAN
from services.kuadran_service import prepare_kuadran_data

TODAY = date.today()
render_sidebar()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Tunggakan AM")

df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()


nama_am = st.text_input("Nama AM", "")
if nama_am:
    filtered_df = df_database[
        df_database["nama_am"].str.contains(nama_am, case=False, na=False)
    ]
else:
    filtered_df = df_database

render_dashboard_metrics(filtered_df)

tab_summary, tab_kuadran = st.tabs(["Summary", "Kuadran"])

filtered_df = filter_collection_data(filtered_df, "-Semua-", tanggal=latest_date)


with tab_summary:
    print_dataframe(filtered_df[COLUMNS_TUNGGAKAN_AM])

with tab_kuadran:
    filtered_df, total_pelanggan, total_saldo = prepare_kuadran_data(
        filtered_df, "-Semua-", COLUMNS_KUADRAN
    )

    render_all_kuadran(filtered_df, total_pelanggan, total_saldo)
    pass

st.divider()
st.subheader("Detail Kuadran")

tab_names = ["Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs, start=1):
    with tab:
        print_dataframe(filtered_df[filtered_df["kuadran"] == i])
