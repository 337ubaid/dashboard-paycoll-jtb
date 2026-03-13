import streamlit as st
from ui.layout import render_sidebar
from ui.metrics import render_dashboard_metrics
from data.database import load_database
from utils.validator import format_currency
from utils.selector import pilih_segmen

render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Dashboard Data Collection Jatim Barat")

df_db_nonpots = load_database()

segmen_target = pilih_segmen()

# METRIC
render_dashboard_metrics(df_db_nonpots, segmen_target)
# SHOW ALL DATA
st.dataframe(format_currency(df_db_nonpots))
