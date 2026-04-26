import streamlit as st

from ui.layout import setup_page
from utils.selector import pilih_all_segmen

setup_page("Supabase","")

db_con = st.connection("supabase")

segmen = "DSS"

segmen_target = pilih_all_segmen()
if segmen_target is None:
    segmen_target = "-Semua-"

df = db_con.query("""
    SELECT idnumber, segmen, saldo_akhir, tanggal
    FROM mybrains_nonpots
    WHERE saldo_akhir > 0  
                  AND tanggal = '2026-04-23'
                  AND segmen = :segmen
""", params={
    "segmen": segmen
}, ttl=60,)

st.dataframe(df)