import streamlit as st

# SpreadSheet
SPREADSHEET_ID = st.secrets["SPREADSHEET_DATABASE"]["spreadsheet_id"]
WORKSHEETS = {
    "collection": st.secrets["SPREADSHEET_DATABASE"]["worksheet_database"],
    "pelanggan": "DATA_PELANGGAN",
}

GCP_SERVICE_ACCOUNT = st.secrets["GCP_SERVICE_ACCOUNT"]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
