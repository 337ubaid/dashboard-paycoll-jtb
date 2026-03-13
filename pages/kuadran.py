import streamlit as st
from ui.layout import render_sidebar
from utils.selector import pilih_segmen
from data.database import load_database_nonpots
from services.filters import filter_collection_data
import streamlit as st
import pandas as pd
from utils.validator import format_currency, print_dataframe, format_skala_rupiah
from datetime import date

TODAY = date.today()
render_sidebar()

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("❇️ Kuadran")

df_database = load_database_nonpots()
segmen_target = pilih_segmen()

df = filter_collection_data(df_database, segmen_target, tanggal=TODAY)

# idnumber, bpname, saldo, AM, keterangan
df = df[["idnumber", "nama_akun", "segmen", "nama_am", "saldo_akhir", "kuadran"]]

total_pelanggan = len(df)
total_saldo = df["saldo_akhir"].sum()


def render_kuadran(kuadran):
    st.subheader(f"Kuadran {kuadran}")
    df_display = df[df["kuadran"] == kuadran]

    total_pelanggan_kuadran = len(df_display)
    total_saldo_kuadran = df_display["saldo_akhir"].sum()

    persen_pelanggan_kuadran = (
        (total_pelanggan_kuadran / total_pelanggan * 100) if total_pelanggan else 0
    )
    persen_saldo_kuadran = (
        (total_saldo_kuadran / total_saldo * 100) if total_saldo else 0
    )

    total_saldo_kuadran = format_skala_rupiah(total_saldo_kuadran)

    c1, c2 = st.columns(2)
    with c1:
        st.write(
            f"Total Pelanggan : {total_pelanggan_kuadran} ({persen_pelanggan_kuadran:.2f}%)"
        )
    with c2:
        st.write(f"Total Saldo : {total_saldo_kuadran} ({persen_saldo_kuadran:.2f}%)")

    print_dataframe(df_display.head(3))
    #
    # st.dataframe(format_currency(df_display))


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
