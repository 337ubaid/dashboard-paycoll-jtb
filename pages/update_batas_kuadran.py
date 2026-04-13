from datetime import date

import pandas as pd
import streamlit as st

from core.rule import BATAS_KUADRAN
from ui.layout import setup_page

TODAY = date.today()

# ====== Konfigurasi Page ======
setup_page("Batas Kuadran", "❇️")
# ==============================

df_batas = (
    pd.DataFrame.from_dict(BATAS_KUADRAN, orient="index")
    .rename_axis("segmen")
    .reset_index()
)

st.dataframe(df_batas)
