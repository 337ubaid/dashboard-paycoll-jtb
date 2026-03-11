import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


spreadsheet_id = st.secrets["SPREADSHEET_DATABASE"]["spreadsheet_id"]
worksheet_name = st.secrets["SPREADSHEET_DATABASE"]["worksheet_name"]

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def get_spreadsheet_client():
    creds = Credentials.from_service_account_info(
        st.secrets["GCP_SERVICE_ACCOUNT"],
        scopes=scope
    )
    return gspread.authorize(creds)


def get_worksheet_object():
    client = get_spreadsheet_client()
    return client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

@st.cache_data(ttl=60)
def get_data_worksheet():
    worksheet_object = get_worksheet_object()
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