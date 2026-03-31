import streamlit as st

from core.config import GCP_SERVICE_ACCOUNT, SCOPE, SPREADSHEET_ID
from data.spreadsheet import (
    get_worksheet_object,
    read_worksheet,
    upsert_mybrains_rows_logic,
)


@st.dialog("Konfirmasi Upload Data")
def confirm_dialog(on_confirm, on_cancel=None):
    if st.session_state.get("show_confirm", False):
        st.warning("Apakah Anda yakin ingin melanjutkan?")

        if st.button("✅ Ya, Upload Sekarang", use_container_width=True):
            on_confirm()
            st.session_state.show_confirm = False
            st.rerun()

        if st.button("❌ Batal", use_container_width=True):
            # if on_cancel:
            #     on_cancel()
            st.session_state.show_confirm = False
            st.rerun()


def upsert_rows_mybrains(df_new, worksheet_name, segmen, tanggal):
    worksheet = get_worksheet_object(SPREADSHEET_ID["nonpots"], worksheet_name)

    df_existing = read_worksheet(SPREADSHEET_ID["nonpots"], worksheet_name)

    result = upsert_mybrains_rows_logic(df_new, worksheet, df_existing, segmen, tanggal)

    if result["mode"] == "init":
        st.success(f"Init data: {result['appended']} baris ditambahkan")
    else:
        if result["deleted"] > 0:
            st.warning(
                f"🗑️ {result['deleted']} baris dihapus untuk {segmen} - {tanggal}"
            )
        else:
            st.info(f"Tidak ada data lama untuk {segmen} - {tanggal}")

        st.success(f"✅ {result['appended']} baris berhasil di-append")
    import time

    with st.spinner("wait"):
        time.sleep(3)
