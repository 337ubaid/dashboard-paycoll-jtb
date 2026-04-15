import streamlit as st

# SpreadSheet database
SPREADSHEET_ID = {
    "nonpots": st.secrets["SPREADSHEET_DATABASE"]["spreadsheet_id"],
    "utip": st.secrets["SPREADSHEET_UTIP"]["spreadsheet_id"],
}

WORKSHEETS_NONPOTS = {
    "collection": "DATABASE",
    "pelanggan": "DATA_PELANGGAN",
    "keterangan": "DATA_KETERANGAN",
}

WORKSHEETS_UTIP = {"utip": "UTIP APRIL"}

WORKSHEETS = {
    **WORKSHEETS_NONPOTS,
    **WORKSHEETS_UTIP,
}
GCP_SERVICE_ACCOUNT = st.secrets["GCP_SERVICE_ACCOUNT"]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
