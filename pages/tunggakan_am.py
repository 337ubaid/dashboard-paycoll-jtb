import streamlit as st
from ui.layout import render_sidebar
from utils.selector import pilih_segmen
from modules.sheets_client import load_database
from modules.metrics import filter_dataframe
import streamlit as st
import pandas as pd
from utils.validator import format_currency, print_dataframe, format_skala_rupiah
from modules.metrics import show_metrics
from datetime import date

TODAY = date.today()
render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Tunggakan AM")

df_database = load_database()
df_database = filter_dataframe(df_database, "-Semua-")

nama_am = st.text_input("Nama AM", "")
if nama_am:
    filtered_df = df_database[
        df_database["nama_am"].str.contains(nama_am, case=False, na=False)
    ]
else:
    filtered_df = df_database

show_metrics(filtered_df)
st.dataframe(filtered_df)
