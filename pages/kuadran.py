import streamlit as st
from core.constant import COLUMNS_KUADRAN
from ui.layout import render_sidebar, render_all_kuadran
from utils.selector import pilih_segmen

from datetime import date


TODAY = date.today()
render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Kuadran")


from services.kuadran_service import prepare_kuadran_data
from ui.layout import render_kuadran
from data.database import load_database_nonpots

df_database = load_database_nonpots()

segmen_target = pilih_segmen()

df, total_pelanggan, total_saldo = prepare_kuadran_data(
    df_database, segmen_target, COLUMNS_KUADRAN
)

render_all_kuadran(df, total_pelanggan, total_saldo)
