from datetime import datetime

import streamlit as st

from utils.schema import SEGMEN, SEGMEN_ONLY


def pilih_all_segmen(key="segmen"):

    return st.selectbox("Pilih Segmen", SEGMEN, key=key)


def pilih_segmen(key="segmen"):

    return st.selectbox("Pilih Segmen", SEGMEN_ONLY, key=key)


def cari_am(df):
    nama_am = st.text_input("Nama AM", "")
    if nama_am:
        filtered_df = df[df["nama_am"].str.contains(nama_am, case=False, na=False)]
    else:
        filtered_df = df
    return filtered_df
