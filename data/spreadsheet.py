import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from core.config import GCP_SERVICE_ACCOUNT, SCOPE, SPREADSHEET_ID


@st.cache_resource
def get_spreadsheet_client():

    creds = Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT, scopes=SCOPE)

    return gspread.authorize(creds)


def get_worksheet_object(spreadsheet_key, worksheet_name):

    client = get_spreadsheet_client()

    return client.open_by_key(spreadsheet_key).worksheet(worksheet_name)


@st.cache_data(ttl=600)
def read_worksheet(spreadsheet_key, worksheet_name):

    worksheet = get_worksheet_object(spreadsheet_key, worksheet_name)

    data = worksheet.get_all_records()

    return pd.DataFrame(data)


import time


def upsert_rows_mybrains(df_new, worksheet_name, segmen, tanggal):
    """
    1. get worksheet data
    2. kalau ada data yg sama (segmen, tanggal) -> hapus
    3. upload data

    """

    df_new["idnumber"] = pd.to_numeric(df_new["idnumber"], errors="coerce").astype(
        "Int64"
    )
    worksheet = get_worksheet_object(SPREADSHEET_ID["nonpots"], worksheet_name)

    df_existing = read_worksheet(SPREADSHEET_ID["nonpots"], worksheet_name)

    if df_existing.empty:
        df_final = df_new

    else:
        df_final = pd.concat([df_existing, df_new], ignore_index=True)

        df_final = df_final.drop_duplicates(
            subset=["tanggal", "segmen", "idnumber"], keep="last"
        )

    with st.spinner("Waiting..."):
        time.sleep(5)
    # st.write(df_existing)
    # confirm_update_database(df_new, tanggal, segmen)
    # worksheet.clear()
    # worksheet.update([df_final.columns.tolist()] + df_final.values.tolist())


def save_new_kuadran(df: pd.DataFrame):

    worksheet = get_worksheet_object(SPREADSHEET_ID["nonpots"], "collection")
    worksheet.clear()

    data = [df.columns.values.tolist()] + df.values.tolist()

    # upload ulang
    worksheet.update(data)
