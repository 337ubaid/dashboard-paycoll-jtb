import streamlit as st
from datetime import datetime
from utils.schema import SEGMEN


def pilih_segmen():
    # Pilihan segmen
    segmen_target = st.selectbox("Pilih Segmen", SEGMEN)
    return segmen_target
