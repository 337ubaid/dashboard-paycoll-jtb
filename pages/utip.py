import streamlit as st

from core.constant import COLUMNS_KUADRAN_UTIP
from data.database import load_database_utip
from services.filters import filter_utip_data
from services.kuadran_service import prepare_data_utip
from ui.kuadran import render_all_kuadran, render_kuadran_utip
from ui.layout import setup_page
from ui.pie import plot_pie
from ui.pivot import pivot_am_keterangan, pivot_periode_utip
from utils.selector import pilih_all_segmen

# ====== Konfigurasi PAge ======
setup_page("UTIP", "❇️")
# ==============================


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

# PIE
st.subheader("Summary Data UTIP")
tab_saldo, tab_customer = st.tabs(["saldo", "customer"])

with tab_saldo:
    fig = plot_pie(df_db_utip, "KET 2", "saldo")
    pivot = pivot_am_keterangan(df_db_utip, "saldo")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Keterangan UTIP")
        st.plotly_chart(fig, width="stretch")
    with col2:
        st.subheader("Tunggakan tiap AM")
        st.dataframe(
            pivot,
            column_config={
                col: st.column_config.NumberColumn(format="%,d")
                for col in pivot.columns
                if col != "nama_am"
            },
            width="stretch",
        )

with tab_customer:
    fig = plot_pie(df_db_utip, "KET 2", "customer")
    pivot = pivot_am_keterangan(df_db_utip, "customer")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Keterangan UTIP")
        st.plotly_chart(fig, width="stretch")
    with col2:
        st.subheader("Tunggakan tiap AM")
        st.dataframe(
            pivot,
            column_config={
                col: st.column_config.NumberColumn(format="%,d")
                for col in pivot.columns
                if col != "nama_am"
            },
            width="stretch",
        )


# KUADRAN
st.divider()
st.subheader("Kuadran")
tab_kuadran, tab_details = st.tabs(["Kuadran", "Detail"])
with tab_kuadran:
    # TODO render ALL KUADRAN buat semua database
    # render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)
    c1, c2 = st.columns(2)
    with c1:
        render_kuadran_utip(df_kuadran, 1, total_pelanggan, total_saldo)
    with c2:
        render_kuadran_utip(df_kuadran, 2, total_pelanggan, total_saldo)

    c3, c4 = st.columns(2)
    with c3:
        render_kuadran_utip(df_kuadran, 3, total_pelanggan, total_saldo)
    with c4:
        render_kuadran_utip(df_kuadran, 4, total_pelanggan, total_saldo)
    st.divider()

with tab_details:
    st.subheader("Detail Data UTIP")
    st.dataframe(df_db_utip)

# PIVOT PERIODE UTIP
# Progressive Corrective

tab_progressive, tab_corrective = st.tabs(["Progressive", "Corrective"])

with tab_progressive:
    st.subheader("Progressive")
    st.dataframe(df_db_utip)
    pivot = pivot_periode_utip(df_db_utip)
    st.dataframe(pivot)
with tab_corrective:
    st.subheader("Corrective")
