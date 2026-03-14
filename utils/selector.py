import streamlit as st
from datetime import datetime
from utils.schema import SEGMEN


def pilih_segmen():
    # Pilihan segmen
    segmen_target = st.selectbox("Pilih Segmen", SEGMEN, index=0, key="segmen_input")
    return segmen_target
