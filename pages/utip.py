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

mode = st.selectbox("Value", ["customer", "saldo"])

fig = plot_pie(df_db_utip, "KET 2", mode)
st.plotly_chart(fig, use_container_width=True)

render_dataframe(df_db_utip)
