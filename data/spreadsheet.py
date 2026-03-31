import time

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


def upsert_mybrains_rows_logic(df_new, worksheet, df_existing, segmen, tanggal):
    df_new = df_new.copy()
    df_new["idnumber"] = pd.to_numeric(df_new["idnumber"], errors="coerce").astype(
        "Int64"
    )

    if df_existing.empty:
        worksheet.update([df_new.columns.tolist()] + df_new.values.tolist())
        return {"deleted": 0, "appended": len(df_new), "mode": "init"}

    df_existing = df_existing.reset_index(drop=True)

    df_existing["tanggal"] = df_existing["tanggal"].astype(str)
    tanggal = str(tanggal)

    mask = (df_existing["tanggal"] == tanggal) & (df_existing["segmen"] == segmen)

    rows_to_delete = df_existing[mask].index.tolist()

    deleted_count = 0

    if rows_to_delete:
        rows_to_delete = sorted([i + 2 for i in rows_to_delete])

        start = min(rows_to_delete)
        end = max(rows_to_delete)

        is_contiguous = rows_to_delete == list(range(start, end + 1))

        if is_contiguous:
            worksheet.delete_rows(start, end)
            deleted_count = len(rows_to_delete)
        else:
            for row_idx in reversed(rows_to_delete):
                worksheet.delete_rows(row_idx)
            deleted_count = len(rows_to_delete)

    worksheet.append_rows(
        df_new.values.tolist(),
        value_input_option="USER_ENTERED",
    )

    return {"deleted": deleted_count, "appended": len(df_new), "mode": "upsert"}


def save_new_kuadran(df: pd.DataFrame):

    worksheet = get_worksheet_object(SPREADSHEET_ID["nonpots"], "collection")
    worksheet.clear()

    data = [df.columns.values.tolist()] + df.values.tolist()

    # upload ulang
    worksheet.update(data)
