import streamlit as st
from modules.components.sidebar import sidebar
from utils.selector import pilih_segmen
from modules.sheets_client import load_database
from modules.metrics import filter_data
import streamlit as st
import pandas as pd
from utils.validator import format_currency,print_dataframe, format_skala_rupiah
from datetime import date


# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈")
st.title("❇️ Tunggakan AM")
sidebar()

df_database = load_database()

nama_am = st.text_input("Nama AM", "")
if nama_am:
    filtered_df = df_database[
        df_database['nama_am'].str.contains(nama_am, case=False, na=False)
    ]
else:
    filtered_df = df_database

st.dataframe(filtered_df)