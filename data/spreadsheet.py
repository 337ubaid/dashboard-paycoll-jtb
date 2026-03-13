import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from core.config import GCP_SERVICE_ACCOUNT, SCOPE, SPREADSHEET_ID


@st.cache_resource
def get_spreadsheet_client():

    creds = Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT, scopes=SCOPE)

    return gspread.authorize(creds)


def get_worksheet(worksheet_name):

    client = get_spreadsheet_client()

    return client.open_by_key(SPREADSHEET_ID).worksheet(worksheet_name)


@st.cache_data(ttl=600)
def read_worksheet(worksheet_name):

    worksheet = get_worksheet(worksheet_name)

    data = worksheet.get_all_records()

    return pd.DataFrame(data)


def append_rows(df, worksheet_name):

    worksheet = get_worksheet(worksheet_name)

    rows = df.values.tolist()

    worksheet.append_rows(rows, value_input_option="USER_ENTERED")
