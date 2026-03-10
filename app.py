import streamlit as st
from modules.components.sidebar import sidebar

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈")
st.title("📈 Dashboard Data Collection Jatim Barat")
sidebar()