import streamlit as st

from core.schema import SEGMEN_ONLY
from data.supabase import get_data_nonpots, get_metric_saldo
from ui.layout import setup_page
from ui.metrics import render_dashboard_metrics_supabase
from utils.selector import pilih_all_segmen

setup_page("Supabase", "")

segmen_target = pilih_all_segmen()
# tanggal = st.date_input("Pilih Tanggal")

conn = st.connection("supabase")

###
filters = {
    "segmen": segmen_target,
}
########## TOTAL SALDO
df = get_metric_saldo(filters)
st.write("df metric saldo")
st.write(df)
render_dashboard_metrics_supabase(df)


########## NONPOTS
df_nonpots = get_data_nonpots(filters)
st.write("df_nonpots")
st.write((df_nonpots))
