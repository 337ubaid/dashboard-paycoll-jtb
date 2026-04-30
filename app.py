import streamlit as st

from data.supabase import get_data_nonpots, get_metric_saldo
from ui.chart import print_chart_tren_saldo_supabase
from ui.layout import print_sort_dataframe, setup_page
from ui.metrics import render_dashboard_metrics_supabase
from utils.selector import pilih_all_segmen

# ====== Konfigurasi Page ======
setup_page("Dashboard Data Collection Jatim Barat", "📈")
# ==============================

segmen_target = pilih_all_segmen()
if segmen_target is None:
    segmen_target = "-Semua-"

filters = {}
if segmen_target != "-Semua-":
    filters["segmen"] = segmen_target

c1, c2 = st.columns(2)
with c1:
    # METRIC
    data_metric = get_metric_saldo(filters)
    render_dashboard_metrics_supabase(data_metric)
with c2:
    # Grafik
    print_chart_tren_saldo_supabase(filters)

# SHOW ALL DATA
df_nonpots = get_data_nonpots(filters)
print_sort_dataframe(df_nonpots)
