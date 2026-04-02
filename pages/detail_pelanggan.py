from datetime import date

import streamlit as st

from data.database import load_database_nonpots
from ui.layout import render_sidebar

TODAY = date.today()
render_sidebar()
df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Detail Pelanggan")
# ==============================
