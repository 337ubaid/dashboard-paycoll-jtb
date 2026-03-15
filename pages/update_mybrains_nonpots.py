import streamlit as st
from ui.layout import render_sidebar
from core.config import WORKSHEETS_NONPOTS
from data.spreadsheet import upsert_rows_mybrains
from data.excel import load_mybrains_excel
from utils.dataframe_utils import normalize_columns
from utils.schema import REQUIRED_COLUMNS_MYBRAINS
from utils.selector import pilih_segmen
from utils.validator import format_currency
from modules.transform import add_metadata, compute_lama_tunggakan, assign_kuadran

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
    file = st.file_uploader("Upload file", type=["xls"], key="upload_file")
    if file:

        try:
            df = load_mybrains_excel(file)
            df = normalize_columns(df)
            df = df[REQUIRED_COLUMNS_MYBRAINS].copy()

            # tambahkan kolom pendukung(segmen, tanggal, kuadran)
            df = add_metadata(df, segmen_target, tanggal)
            df = compute_lama_tunggakan(df)
            df = assign_kuadran(df)
            st.dataframe(format_currency(df))

        except Exception as e:
            st.error(str(e))


if st.button("Upload ke Database", type="primary"):

    upsert_rows_mybrains(df, WORKSHEETS_NONPOTS["collection"])
    st.cache_data.clear()
    # if "upload_file" in st.session_state:
    #     del st.session_state["upload_file"]
    # if "segmen_input" in st.session_state:
    #     del st.session_state["segmen_input"]

    st.success("Data berhasil diupload")

    # st.switch_page("pages/kuadran.py")
    # st.switch_page("pages/update_mybrains_nonpots.py")
