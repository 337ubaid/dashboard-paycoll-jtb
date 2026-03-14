from core.schema import ALL_SCHEMAS


# def format_headers(df):
#     df = df.copy()
#     df.columns = df.columns.str.replace("_", " ").str.upper()
#     return df


def format_headers(df):
    return {c: c.replace("_", " ").upper() for c in df.columns}


def format_currency(df):
    cols = get_currency_columns(df)
    return df.style.format({c: "{:,.0f}" for c in cols})


import streamlit as st


def get_currency_columns(df):
    cols = [
        col for col, t in ALL_SCHEMAS.items() if t == "currency" and col in df.columns
    ]
    return cols


def format_skala_rupiah(x):
    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.1f} M"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.1f} Jt"
    elif x >= 1_000:
        return f"{x/1_000:.1f} Rb"
    else:
        return f"{x:.0f}"
