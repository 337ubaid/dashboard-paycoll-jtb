import pandas as pd
import streamlit as st
from utils.formatter import format_currency


def format_skala_rupiah(x):
    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.1f} M"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.1f} Jt"
    elif x >= 1_000:
        return f"{x/1_000:.1f} Rb"
    else:
        return f"{x:.0f}"


def print_dataframe(df):
    df = df.sort_values("saldo_akhir", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df = format_currency(df)
    st.dataframe(df)
