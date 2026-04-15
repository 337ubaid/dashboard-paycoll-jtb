import streamlit as st

from core.config import SPREADSHEET_ID, WORKSHEETS
from data.spreadsheet import read_worksheet
from utils.parser import parse_dataframe


@st.cache_data(ttl=600)
def load_database_nonpots():
    df_collection = load_database(SPREADSHEET_ID["nonpots"], "collection")
    df_pelanggan = load_database(
        SPREADSHEET_ID["nonpots"], "pelanggan", ["idnumber", "nama_am", "nama_akun"]
    )
    df_keterangan = load_database(SPREADSHEET_ID["nonpots"], "keterangan")

    df = df_collection.merge(df_pelanggan, on="idnumber", how="left")
    df = df.merge(df_keterangan, on="idnumber", how="left")

    return df


@st.cache_data(ttl=600)
def load_database_utip():
    df = load_database(
        SPREADSHEET_ID["utip"],
        "utip",
        [
            "BULAN UTIP",
            "PAYMENT-ID",
            "SEGMEN",
            "DATE",
            "MONTH",
            "Periode UTIP",
            "ACCTNO",
            "STANDART CUSTOMER NAME",
            "SALDO AWAL",
            "saldo_akhir",
            "KET",
            "KET 2",
            "nama_am",
            "kuadran",
        ],
    )
    return df


@st.cache_data(ttl=600)
def load_database(
    spreadsheet_key, database_name, columns: list[str] | str | None = None
):
    df = read_worksheet(spreadsheet_key, WORKSHEETS[database_name])
    df = parse_dataframe(df, database_name)
    if columns is None:
        return df
    return df[columns]
