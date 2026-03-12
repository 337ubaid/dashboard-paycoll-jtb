import streamlit as st
from modules.components.sidebar import sidebar
from modules.sheets_client import load_database
from utils.validator import format_currency
import streamlit as st
import pandas as pd
from utils.selector import pilih_segmen
from modules.metrics import show_metrics

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈")
st.title("📈 Dashboard Data Collection Jatim Barat")
sidebar()

df_database = load_database()

segmen_target = pilih_segmen()



# METRIC
show_metrics(df_database, segmen_target)
# SHOW ALL DATA
st.dataframe(format_currency(df_database))