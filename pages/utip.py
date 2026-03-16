import streamlit as st
from ui.layout import render_sidebar, render_dataframe, render_kuadran_utip

render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ UTIP")


from data.database import load_database_utip
from utils.selector import pilih_segmen
from services.filters import filter_utip_data

df_db_utip = load_database_utip()
segmen_target = pilih_segmen()

df_db_utip = filter_utip_data(df_db_utip, segmen_target)


from ui.pie import plot_pie
from ui.pivot import pivot_am_keterangan

mode = st.selectbox("Total", ["saldo", "customer"])
# mode = st.segmented_control("Total", ["customer", "saldo"])

fig = plot_pie(df_db_utip, "KET 2", mode)
pivot = pivot_am_keterangan(df_db_utip, mode)


from core.constant import COLUMNS_KUADRAN_UTIP
from services.kuadran_service import prepare_kuadran_utip

df, total_pelanggan, total_saldo = prepare_kuadran_utip(
    df_db_utip, COLUMNS_KUADRAN_UTIP
)

# PIE
col1, col2 = st.columns(2)
with col1:
    c1, c2 = st.columns(2)
    c1.metric("Total UTIP", f"{total_saldo:,.0f}")
    c2.metric("Total Payment ID", f"{total_pelanggan:,.0f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribusi Keterangan UTIP")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Tunggakan tiap AM")
    st.dataframe(
        pivot,
        column_config={
            col: st.column_config.NumberColumn(format="%,d")
            for col in pivot.columns
            if col != "AM"
        },
        use_container_width=True,
    )


# KUADRAN
st.divider()
c1, c2 = st.columns(2)
with c1:
    render_kuadran_utip(df, 1, total_pelanggan, total_saldo)
with c2:
    render_kuadran_utip(df, 2, total_pelanggan, total_saldo)

c3, c4 = st.columns(2)
with c3:
    render_kuadran_utip(df, 3, total_pelanggan, total_saldo)
with c4:
    render_kuadran_utip(df, 4, total_pelanggan, total_saldo)
st.divider()


st.subheader("Detail Data UTIP")
st.dataframe(df_db_utip)
