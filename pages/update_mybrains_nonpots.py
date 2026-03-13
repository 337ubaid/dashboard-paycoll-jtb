import streamlit as st
from ui.layout import render_sidebar
from modules.transform import add_metadata, compute_lama_tunggakan, assign_kuadran
from modules.excel_reader import read_excel_mybrains
from modules.cleaner import clean_header
from utils.schema import REQUIRED_COLUMNS_MYBRAINS
from utils.selector import pilih_segmen
from data.spreadsheet import append_rows
from utils.validator import format_currency
from core.config import WORKSHEETS

render_sidebar()
# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("📈 Update MyBrains NonPots")

col1, col2 = st.columns(2)

with col2:
    segmen_target = pilih_segmen()
    tanggal = st.date_input("Bill Periode", value="today")
    tanggal = tanggal.strftime("%d/%m/%Y")

with col1:
    file = st.file_uploader("Upload file", type=["xls"])
    if file:

        try:
            df = read_excel_mybrains(file)
            df = clean_header(df)
            df = df[REQUIRED_COLUMNS_MYBRAINS].copy()

            # tambahkan kolom pendukung(segmen, tanggal, kuadran)
            df = add_metadata(df, segmen_target, tanggal)
            df = compute_lama_tunggakan(df)
            df = assign_kuadran(df)
            st.dataframe(format_currency(df))

        except Exception as e:
            st.error(str(e))


if st.button("Upload ke Database", type="primary"):

    append_rows(df, WORKSHEETS["collection"])
    st.cache_data.clear()
    st.success("Data berhasil diupload")
