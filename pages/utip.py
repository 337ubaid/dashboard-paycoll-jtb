import streamlit as st

from core.constant import COLUMNS_KUADRAN_UTIP
from data.database import load_database_utip
from services.filters import filter_utip_data
from services.kuadran_service import prepare_data_utip
from ui.kuadran import render_all_kuadran, render_kuadran_utip
from ui.layout import setup_page, summary_data_utip
from ui.pie import plot_pie_utip
from ui.pivot import pivot_am_keterangan, pivot_periode_utip
from utils.selector import pilih_all_segmen

setup_page("UTIP", "❏️")


df_db_utip = load_database_utip()
segmen_target = pilih_all_segmen()

df_db_utip = filter_utip_data(df_db_utip, segmen_target)

df_kuadran, total_pelanggan, total_saldo = prepare_data_utip(
    df_db_utip, COLUMNS_KUADRAN_UTIP
)

col1, col2 = st.columns(2)
with col1:
    c1, c2 = st.columns(2)
    c1.metric("Total UTIP", f"{total_saldo:,.0f}")
    c2.metric("Total Payment ID", f"{total_pelanggan:,.0f}")

st.divider()
st.subheader("Summary Data UTIP")
tab_saldo, tab_customer = st.tabs(["saldo", "customer"])

with tab_saldo:
    summary_data_utip(df_db_utip, "saldo")
with tab_customer:
    summary_data_utip(df_db_utip, "customer")


st.divider()
st.subheader("Kuadran")
tab_kuadran, tab_details = st.tabs(["Kuadran", "Detail"])

with tab_kuadran:
    render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)
    st.divider()
with tab_details:
    st.subheader("Detail Data UTIP")
    st.dataframe(df_db_utip)

st.divider()
tab_progressive, tab_corrective = st.tabs(["Progressive", "Corrective"])

with tab_progressive:
    st.subheader("Progressive")
    st.dataframe(df_db_utip)
    pivot = pivot_periode_utip(df_db_utip)
    st.dataframe(pivot)
with tab_corrective:
    st.subheader("Corrective")
