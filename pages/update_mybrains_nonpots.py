import streamlit as st
from modules.components.sidebar import sidebar
from modules.transform import add_metadata, compute_lama_tunggakan, assign_kuadran
from modules.excel_reader import read_excel_mybrains
from modules.cleaner import clean_header
from utils.schema import REQUIRED_COLUMNS_MYBRAINS
from utils.selector import pilih_kategori

# ====== Konfigurasi PAge ======
st.set_page_config(
    page_title="Update MyBrains NonPots", layout="wide", page_icon=":material/event_repeat:")
st.title("📈 Update MyBrains NonPots")
sidebar()

# TASK
# ✅ 1. upload excel 
# ✅ 2. baca excel
# ✅ 3. bersihkan data excel
# ✅ 4. tampilkan data yang sudah bersih
# 5. update data ke database
# 6. konfirmasi kirim

bulan_target, tahun_target, segmen_target = pilih_kategori()
bill_periode = f"{tahun_target}{bulan_target:02d}"

file = st.file_uploader("Upload file", type=["xls"])
if file:

    try:
        df = read_excel_mybrains(file)
        df = clean_header(df)
        df = df[REQUIRED_COLUMNS_MYBRAINS].copy()
        
        # tambahkan kolom pendukung(segmen, billper, kuadran)
        df = add_metadata(df, segmen_target, bill_periode)
        df = compute_lama_tunggakan(df)
        df = assign_kuadran(df)
        st.dataframe(df)

        # if st.button("Upload ke database"):
            # upload_to_sheet(df)
            # st.success("Data berhasil diupload")

    except Exception as e:
        st.error(str(e))