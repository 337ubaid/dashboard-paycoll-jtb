from datetime import date

import streamlit as st

from data.database import load_database_nonpots
from ui.layout import setup_page

TODAY = date.today()

df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()

# ====== Konfigurasi Page ======

setup_page("Detail Pelanggan", "🧩")
# ==============================
