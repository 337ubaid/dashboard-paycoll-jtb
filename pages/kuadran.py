import streamlit as st
from core.constant import COLUMNS_KUADRAN, TODAY
from ui.layout import render_sidebar, render_all_kuadran, print_sort_dataframe
from utils.selector import pilih_segmen
from services.kuadran_service import prepare_kuadran_data
from data.database import load_database_nonpots


render_sidebar()
df_database = load_database_nonpots()

# ====== Konfigurasi Page ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Kuadran")
# ==============================

# ====== Select Segmen ======
segmen_target = pilih_segmen()

df, total_pelanggan, total_saldo = prepare_kuadran_data(
    df_database, segmen_target, COLUMNS_KUADRAN
)

# ====== Print Kuadran ======
render_all_kuadran(df, total_pelanggan, total_saldo)

# ====== Detail Kuadran ======
# TODO jadikan fungsi
st.divider()
st.subheader("Detail Kuadran")

tab_names = ["Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs, start=1):
    with tab:
        print_sort_dataframe(df[df["kuadran"] == i])
