from datetime import datetime

import streamlit as st

from core.schema import SEGMEN, SEGMEN_ONLY


def pilih_all_segmen(key="segmen"):

    return st.selectbox("Pilih Segmen", SEGMEN, key=key)


def pilih_segmen(key="segmen"):

    return st.selectbox("Pilih Segmen", SEGMEN_ONLY, key=key)


def cari_am(df, nama_am):
    if not nama_am:
        return df

    return df[df["nama_am"].str.contains(nama_am, case=False, na=False)]


def input_am():
    return st.text_input("Nama AM", "")
