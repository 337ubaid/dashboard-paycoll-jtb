import streamlit as st
from ui.layout import render_sidebar
import streamlit as st
import pandas as pd
from datetime import date
from core.rule import BATAS_KUADRAN

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
