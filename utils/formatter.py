from core.schema import ALL_SCHEMAS


def format_headers(df):
    """Format dataframe headers to UPPERCASE and replace underscores with spaces."""
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


def format_skala_rupiah(number):
    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.1f} M"
    elif number >= 1_000_000:
        return f"{number/1_000_000:.1f} Jt"
    elif number >= 1_000:
        return f"{number/1_000:.1f} Rb"
    else:
        return f"{number:.0f}"
