import streamlit as st

# SpreadSheet database
SPREADSHEET_ID = {
    "nonpots": st.secrets["SPREADSHEET_DATABASE"]["spreadsheet_id"],
    "utip": st.secrets["SPREADSHEET_UTIP"]["spreadsheet_id"],
}

WORKSHEETS_NONPOTS = {
    "collection": st.secrets["SPREADSHEET_DATABASE"]["worksheet_database"],
    "pelanggan": "DATA_PELANGGAN",
}

GCP_SERVICE_ACCOUNT = st.secrets["GCP_SERVICE_ACCOUNT"]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
