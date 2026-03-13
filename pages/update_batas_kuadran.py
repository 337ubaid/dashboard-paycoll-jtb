import streamlit as st
from ui.layout import render_sidebar
from utils.selector import pilih_segmen
from modules.sheets_client import load_database
from modules.metrics import filter_dataframe
import streamlit as st
import pandas as pd
from utils.validator import format_currency, print_dataframe, format_skala_rupiah
from datetime import date
from utils.schema import BATAS_KUADRAN

TODAY = date.today()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Update Kuadran")
render_sidebar()

df_batas = (
    pd.DataFrame.from_dict(BATAS_KUADRAN, orient="index")
    .rename_axis("segmen")
    .reset_index()
)

st.dataframe(df_batas)
