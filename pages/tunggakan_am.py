import streamlit as st
from ui.layout import render_sidebar, render_dataframe
from data.database import load_database_nonpots
from services.filters import filter_collection_data
from ui.metrics import render_dashboard_metrics
from datetime import date
from core.constant import COLUMNS_TUNGGAKAN_AM

TODAY = date.today()
render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Tunggakan AM")

df_database = load_database_nonpots()
latest_date = df_database["tanggal"].max()


nama_am = st.text_input("Nama AM", "")
if nama_am:
    filtered_df = df_database[
        df_database["nama_am"].str.contains(nama_am, case=False, na=False)
    ]
else:
    filtered_df = df_database

render_dashboard_metrics(filtered_df)
filtered_df = filter_collection_data(filtered_df, "-Semua-", tanggal=latest_date)
filtered_df = filtered_df[COLUMNS_TUNGGAKAN_AM]
filtered_df.index = filtered_df.reset_index(drop=True).index + 1
render_dataframe(filtered_df)
