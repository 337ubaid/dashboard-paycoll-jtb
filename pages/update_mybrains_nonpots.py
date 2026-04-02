import streamlit as st

from core.config import WORKSHEETS_NONPOTS
from core.constant import TODAY
from ui.dialog import confirm_dialog, upsert_rows_mybrains
from ui.layout import print_sort_dataframe, render_sidebar
from utils.dataframe_utils import convert_excel_mybrains_nonpots, create_empty_df
from utils.selector import pilih_segmen
from utils.validator import format_currency

render_sidebar()
# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Dashboard Data Collection Jatim Barat", layout="wide", page_icon="📈"
)
st.title("🧠 Update MyBrains NonPots")


# Init Session
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1
if "tanggal" not in st.session_state:
    st.session_state.tanggal = TODAY
if "segmen" not in st.session_state:
    st.session_state.segmen = None

# Columns Show
col_selector, col_dataframe = st.columns(2)

with col_selector:
    segmen_target = pilih_segmen(key="segmen")
    tanggal = st.date_input("Bill Periode", key="tanggal")
    tanggal = tanggal.strftime("%d/%m/%Y")
    file = st.file_uploader(
        "Upload file",
        type=["xls"],
        key=st.session_state["uploader_key"],
    )

    if file and segmen_target:
        df_upload = convert_excel_mybrains_nonpots(file, segmen_target, tanggal)
        st.session_state.df_upload = df_upload
        st.info(
            f"Terdapat **{len(df_upload)}** baris data untuk segmen **{segmen_target}**"
        )

with col_dataframe:
    if file and segmen_target and tanggal:
        try:
            print_sort_dataframe(df_upload)

        except Exception as e:
            st.error(str(e))

    else:
        st.dataframe(create_empty_df())


is_valid = st.session_state.segmen is not None and file is not None


# TODO : buat modular biar clean
def clear_form():
    st.session_state["uploader_key"] += 1
    st.session_state.tanggal = TODAY
    st.session_state.segmen = None


def handle_upload():
    df_upload = st.session_state.get("df_upload")
    upsert_rows_mybrains(
        df_upload, WORKSHEETS_NONPOTS["collection"], segmen_target, tanggal
    )
    clear_form()


if st.button(
    "Upload ke Database",
    type="primary",
    disabled=not is_valid,
):
    st.session_state.show_confirm = True
    confirm_dialog(on_confirm=handle_upload)
