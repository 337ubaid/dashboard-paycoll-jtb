import pandas as pd
import streamlit as st

def get_data_formatted(df):
    # st.write(df)
    # format tanggal
    df["tanggal"] = pd.to_datetime(
        df["tanggal"],
        format="%d/%m/%Y"
    ).dt.date
    # st.write(df)
    return df

def format_currency(df):

    cols = [
        "saldo_akhir",
        "0-3_bln",
        "4-6_bln",
        "7-12_bln",
        "13-24_bln",
        ">_24_bln"
    ]

    return df.style.format({c: "{:,.0f}" for c in cols})