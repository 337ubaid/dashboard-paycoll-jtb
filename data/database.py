import streamlit as st

from core.config import SPREADSHEET_ID, WORKSHEET
from data.spreadsheet import read_worksheet
from utils.parser import parse_dataframe


@st.cache_data(ttl=600)
def load_database_nonpots():
    df_collection = load_database(SPREADSHEET_ID["nonpots"], "collection")
    df_pelanggan = load_database(SPREADSHEET_ID["nonpots"], "pelanggan")

    df = df_collection.merge(df_pelanggan, on="idnumber", how="left")

    return df


@st.cache_data(ttl=600)
def load_database_utip():
    df = load_database(SPREADSHEET_ID["utip"], "utip")
    return df


@st.cache_data(ttl=600)
def load_database(spreadsheet_key, database_name):
    df = read_worksheet(spreadsheet_key, WORKSHEET[database_name])
    df = parse_dataframe(df, database_name)
    return df
