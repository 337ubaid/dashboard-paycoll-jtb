from datetime import date

import pandas as pd
import streamlit as st

from core.rule import BATAS_KUADRAN
from ui.layout import render_dataframe, render_sidebar

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

from data.database import load_database_nonpots
from services.kuadran_service import assign_kuadran

df = load_database_nonpots()

df = assign_kuadran(df)

render_dataframe(df)
