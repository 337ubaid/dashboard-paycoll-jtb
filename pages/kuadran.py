import streamlit as st
from modules.components.sidebar import sidebar
from utils.selector import pilih_segmen
from modules.sheets_client import load_database
from modules.metrics import filter_data
import streamlit as st
import pandas as pd
from utils.validator import format_currency
from datetime import date

TODAY = date.today()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Kuadran", layout="wide", page_icon="❇️")
st.title("❇️ Kuadran")
sidebar()

df_database = load_database()

segmen_target = pilih_segmen()

def render_kuadran(kuadran):
    st.subheader(f"Kuadran {kuadran}")
    df_display = filter_data(df_database, segmen_target, kuadran=kuadran, tanggal=TODAY   )
    # idnumber, bpname, saldo, AM, keterangan
    df_display = df_display[[
        "idnumber",
        "nama_akun",
        "segmen",
        "nama_am",
        "saldo_akhir",
        "kuadran"
    ]]
    st.dataframe(format_currency(df_display))
    pass

c1, c2 = st.columns(2)
with c1:
    render_kuadran(1)
with c2:
    render_kuadran(2)

c3, c4 = st.columns(2)
with c3:
    render_kuadran(3)
with c4:
    render_kuadran(4)


