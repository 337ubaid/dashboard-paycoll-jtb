import streamlit as st

from data.spreadsheet import read_worksheet
from core.config import WORKSHEETS
from utils.validator import get_data_formatted


@st.cache_data(ttl=600)
def load_database():

    df_collection = read_worksheet(WORKSHEETS["collection"])
    df_collection = get_data_formatted(df_collection)

    df_pelanggan = read_worksheet(WORKSHEETS["pelanggan"])

    df = df_collection.merge(df_pelanggan, on="idnumber", how="left")

    return df
