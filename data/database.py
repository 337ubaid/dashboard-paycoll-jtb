import streamlit as st

from data.spreadsheet import read_worksheet
from core.config import SPREADSHEET_ID, WORKSHEETS_NONPOTS
from utils.validator import get_data_formatted


@st.cache_data(ttl=600)
def load_database_nonpots():
    spreadsheet_key = SPREADSHEET_ID["nonpots"]
    df_collection = read_worksheet(spreadsheet_key, WORKSHEETS_NONPOTS["collection"])
    df_collection = get_data_formatted(df_collection)

    df_pelanggan = read_worksheet(spreadsheet_key, WORKSHEETS_NONPOTS["pelanggan"])

    df = df_collection.merge(df_pelanggan, on="idnumber", how="left")
    return df


@st.cache_data(ttl=600)
def load_database_utip():
    spreadsheet_key = SPREADSHEET_ID["utip"]
    df = read_worksheet(spreadsheet_key, "UTIP MARET")
    return df
