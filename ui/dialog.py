import streamlit as st
import time

from core.config import GCP_SERVICE_ACCOUNT, SCOPE, SPREADSHEET_ID
# from data.spreadsheet import (
#     get_worksheet_object,
#     read_worksheet,
#     upsert_mybrains_rows_logic,
# )
from data.supabase import upsert_mybrains_nonpots_supabase


@st.dialog("Konfirmasi Upload Data")
def confirm_dialog(on_confirm, on_cancel=None):
    if st.session_state.get("show_confirm", False):
        st.warning("Apakah Anda yakin ingin melanjutkan?")

        if st.button("✅ Ya, Upload Sekarang", width="stretch"):
            on_confirm()
            st.session_state.show_confirm = False
            st.cache_data.clear()
            st.rerun()

        if st.button("❌ Batal", width="stretch"):
            # if on_cancel:
            #     on_cancel()
            st.session_state.show_confirm = False
            st.rerun()


def upsert_rows_mybrains(df_new, worksheet_name, segmen, tanggal):
    """
    Upsert data MyBrains NonPots ke Supabase.
    
    Args:
        df_new: DataFrame dengan data baru
        worksheet_name: Nama worksheet (untuk kompatibilitas, tidak digunakan saat ini)
        segmen: Segmen pelanggan / "-Semua-" untuk semua segmen
        tanggal: Tanggal periode (format DD/MM/YYYY)
    """
    
    # TODO: Google Sheets upload (legacy)
    # worksheet = get_worksheet_object(SPREADSHEET_ID["nonpots"], worksheet_name)
    # df_existing = read_worksheet(SPREADSHEET_ID["nonpots"], worksheet_name)
    # result = upsert_mybrains_rows_logic(df_new, worksheet, df_existing, segmen, tanggal)
        #
    # if result["mode"] == "init":
    #     st.success(f"Init data: {result['appended']} baris ditambahkan")
    # else:
    #     if result["deleted"] > 0:
    #         st.warning(
    #             f"🗑️ {result['deleted']} baris dihapus untuk {segmen} - {tanggal}"
    #         )
    #     else:
    #         st.info(f"Tidak ada data lama untuk {segmen} - {tanggal}")
    #
    #     st.success(f"✅ {result['appended']} baris berhasil di-append")
    # ====================================================================
    
    # Current: Upload ke Supabase
    with st.spinner("Uploading to Supabase..."):
        result = upsert_mybrains_nonpots_supabase(df_new, segmen, tanggal)
        time.sleep(30)
    
    if result["success"]:
        st.success(f"✅ {result['upserted']} baris berhasil di-upload ke Supabase")
    else:
        st.error(f"❌ Gagal upload ke Supabase: {result['error']}")
