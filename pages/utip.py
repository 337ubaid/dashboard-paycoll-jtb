import streamlit as st
from ui.layout import render_sidebar

render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ UTIP")


from data.database import load_database_utip

st.dataframe(load_database_utip())
