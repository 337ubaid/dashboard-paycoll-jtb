import streamlit as st
from datetime import datetime
from utils.schema import SEGMEN


def pilih_segmen():
    # Pilihan segmen
    segmen_target = st.selectbox("Pilih Segmen", SEGMEN, key="segmen_input")
    return segmen_target
