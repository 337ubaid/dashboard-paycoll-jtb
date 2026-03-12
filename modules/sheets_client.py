import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from utils.validator import get_data_formatted

spreadsheet_id = st.secrets["SPREADSHEET_DATABASE"]["spreadsheet_id"]
worksheet_database = st.secrets["SPREADSHEET_DATABASE"]["worksheet_database"]

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_data(ttl=600)
def load_database():
    df_collection = get_data_worksheet(worksheet_database)
    df_collection = get_data_formatted(df_collection)

    df_pelanggan = get_data_worksheet("DATA_PELANGGAN")
    df = df_collection.merge(
        df_pelanggan,
        on="idnumber",
        how="left"
    )

    return df

@st.cache_resource
def get_spreadsheet_client():
    creds = Credentials.from_service_account_info(
        st.secrets["GCP_SERVICE_ACCOUNT"],
        scopes=scope
    )
    return gspread.authorize(creds)


def get_worksheet_object(worksheet_name):
    client = get_spreadsheet_client()
    return client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

@st.cache_data(ttl=60)
def get_data_worksheet(worksheet_name):
    worksheet_object = get_worksheet_object(worksheet_name)
    data = worksheet_object.get_all_records()
    df_db = pd.DataFrame(data)
    return df_db

def upload_data_to_sheet(df):

    worksheet = get_worksheet_object()

    rows = df.values.tolist()

    worksheet.append_rows(
        rows,
        value_input_option="USER_ENTERED"
    )