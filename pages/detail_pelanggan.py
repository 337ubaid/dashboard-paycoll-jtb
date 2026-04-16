from datetime import date

import streamlit as st

from core.constant import COLUMNS_KUADRAN, COLUMNS_TUNGGAKAN_AM
from data.database import load_database_nonpots
from services.filters import filter_collection_data
from services.kuadran_service import prepare_kuadran_data
from ui.chart import print_chart_tren_saldo
from ui.kuadran import render_all_kuadran
from ui.layout import print_sort_dataframe, setup_page
from ui.metrics import render_dashboard_metrics
from utils.selector import cari_am, input_am, pilih_all_segmen

TODAY = date.today()

df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()

# ====== Konfigurasi Page ======
setup_page("Detail Pelanggan", "❇️")
# ==============================

# FILTERING

c1, c2, c3 = st.columns(3)
with c1:
    segmen_target = pilih_all_segmen()
with c2:
    nama_am = input_am()
with c3:
    pass

filtered_df = cari_am(df_database, nama_am)

st.header("📌 Summary")
c1, c2 = st.columns(2)
# METRICS
with c1:
    render_dashboard_metrics(filtered_df, segmen_target)
with c2:
    print_chart_tren_saldo(filtered_df, segmen_target)

# KUADRAN & SUMMARY
st.header(
    "📌 Kuadran",
    help="Pengelompokkan prioritas pelanggan berdasarkan besar **Nilai Pinjaman** dan **Lama Tunggakan**",
)
tab_kuadran, tab_details = st.tabs(["Kuadran", "Detail"])
filtered_df = filter_collection_data(filtered_df, segmen_target, tanggal=latest_date)

with tab_kuadran:
    df_kuadran, total_pelanggan, total_saldo = prepare_kuadran_data(
        filtered_df, segmen_target, COLUMNS_KUADRAN
    )

    render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)
with tab_details:
    # DETAIL KUADRAN
    st.subheader("Detail Kuadran")
    # print_sort_dataframe(filtered_df[COLUMNS_TUNGGAKAN_AM])

    tab_names = ["ALL", "Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            if i == 0:
                df_show = filtered_df
            else:
                df_show = filtered_df[filtered_df["kuadran"] == i]
            st.info(f"{len(df_show)} Pelanggan")
            print_sort_dataframe(df_show)

# UTIP
st.divider()
st.header(
    "📌 UTIP",
    help="Uang Titipan",
)
from data.database import load_database_utip

df_db_utip = load_database_utip()
filtered_df_utip = cari_am(df_db_utip, nama_am)
st.dataframe(filtered_df_utip)
