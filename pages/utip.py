import streamlit as st
from ui.layout import render_sidebar, render_dataframe

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

mode = st.selectbox("Total", ["customer", "saldo"])

fig = plot_pie(df_db_utip, "KET 2", mode)
pivot = pivot_am_keterangan(df_db_utip)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Keterangan UTIP")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Tunggakan tiap AM")
    st.dataframe(pivot, use_container_width=True)
st.subheader("Detail Data UTIP")
render_dataframe(df_db_utip)
