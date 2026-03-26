import streamlit as st
from datetime import datetime
from utils.schema import SEGMEN


def pilih_segmen():
    # Pilihan segmen
    segmen_target = st.selectbox("Pilih Segmen", SEGMEN, key="segmen_input")
    return segmen_target


def cari_am(df):
    nama_am = st.text_input("Nama AM", "")
    if nama_am:
        filtered_df = df[df["nama_am"].str.contains(nama_am, case=False, na=False)]
    else:
        filtered_df = df
    return filtered_df
