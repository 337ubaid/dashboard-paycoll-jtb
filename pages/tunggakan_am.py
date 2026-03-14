import streamlit as st
from ui.layout import render_sidebar, render_dataframe
from data.database import load_database_nonpots
from services.filters import filter_collection_data
from ui.metrics import render_dashboard_metrics
from datetime import date

TODAY = date.today()
render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Tunggakan AM")

df_database = load_database_nonpots()
df_database = filter_collection_data(df_database, "-Semua-")

nama_am = st.text_input("Nama AM", "")
if nama_am:
    filtered_df = df_database[
        df_database["nama_am"].str.contains(nama_am, case=False, na=False)
    ]
else:
    filtered_df = df_database

render_dashboard_metrics(filtered_df)
render_dataframe(filtered_df)
