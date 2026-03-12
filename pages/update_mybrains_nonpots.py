import streamlit as st
from modules.components.sidebar import sidebar
from modules.transform import add_metadata, compute_lama_tunggakan, assign_kuadran
from modules.excel_reader import read_excel_mybrains
from modules.cleaner import clean_header
from utils.schema import REQUIRED_COLUMNS_MYBRAINS
from utils.selector import pilih_segmen
from modules.sheets_client import upload_data_to_sheet
from utils.validator import format_currency

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

            # if st.button("Upload ke database"):
                # upload_to_sheet(df)
                # st.success("Data berhasil diupload")

        except Exception as e:
            st.error(str(e))


if st.button("Upload ke Database", type="primary"):

    upload_data_to_sheet(df)
    st.cache_data.clear()
    st.success("Data berhasil diupload")

# from streamlit_extras.stylable_container import stylable_container

# # Create buttons with st.button
# with stylable_container(
#     "green",
#     css_styles="""
#     button {
#         background-color: #00FF00;
#         color: black;
#     }""",
# ):
#     button1_clicked = st.button("Button 1", key="button1")
# with stylable_container(
#     "red",
#     css_styles="""
#     button {
#         background-color: #FF0000;

#     }""",
# ):
#     button2_clicked = st.button("Button 2", key="button2")

# # Check button states and print messages
# if st.button("Submit"):
#     if button1_clicked:
#         st.write("Button 1 pressed")
#     elif button2_clicked:
#         st.write("Button 2 pressed")

