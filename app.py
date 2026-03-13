import streamlit as st
from data.database import load_database_nonpots
from ui.layout import render_sidebar
from ui.metrics import render_dashboard_metrics
from utils.validator import format_currency
from utils.selector import pilih_segmen
from services.filters import filter_collection_data
from core.constant import TODAY

render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Dashboard Data Collection Jatim Barat")

df_db_nonpots = load_database_nonpots()

segmen_target = pilih_segmen()

# METRIC
render_dashboard_metrics(df_db_nonpots, segmen_target)
# SHOW ALL DATA
df_db_nonpots = filter_collection_data(df_db_nonpots, segmen_target, tanggal=TODAY)
st.dataframe(format_currency(df_db_nonpots))
