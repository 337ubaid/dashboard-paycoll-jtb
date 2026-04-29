import pandas as pd
import streamlit as st
from datetime import datetime

from data.database import load_database_nonpots
from data.supabase import get_database_cr_cyc
from services.filters import filter_column
from ui.layout import setup_page
from utils.selector import pilih_all_segmen

setup_page("CR CYC Performance", "🗓️")

segmen = pilih_all_segmen()
if segmen is None:
    segmen = "Total"

df_cr, df_target_cr, df_cyc, df_target_cyc = get_database_cr_cyc(segmen)

def metric_cr_cyc(cr_cyc, now, target, shortage, metric_label="CR"):
    st.header(cr_cyc)
    c1, c2 = st.columns(2)
    c1.metric(f"Total {metric_label}", f"{now:.2%}", delta=f"{now - target:.2%}", delta_arrow="off")
    c2.metric(f"Target {metric_label}", f"{target:.2%}")
    st.metric("Shortage", shortage)

def count_shortage(diff_cr, bill_total, bill_bjt, cash_bjt):
    return diff_cr * (bill_total - bill_bjt + cash_bjt) * -1_000_000_000

def get_metric_data(df, df_target, metric_type, segmen, month_column):
    """Extract metric data from dataframes"""
    value_col = f"{metric_type} CASH" if metric_type == "CYC" else "CR CASH"
    bill_col = "BILL" if metric_type == "CYC" else "BILL (TOTAL)"
    
    now = df[df['UBIS'] == segmen][value_col].values[0]
    target_row = df_target[df_target['SEGMEN'] == segmen]
    target = target_row[month_column].values[0] if not target_row.empty and month_column in target_row.columns else 0.0
    
    bill_total = df[df['UBIS'] == segmen][bill_col].values[0]
    bill_bjt = df[df['UBIS'] == segmen]['BILL BJT'].values[0]
    cash_bjt = df[df['UBIS'] == segmen]['CASH BJT'].values[0]
    
    diff = target - now
    shortage = count_shortage(diff, bill_total, bill_bjt, cash_bjt)
    return now, target, f"Rp {shortage:,.0f}", shortage

month_column = str(datetime.now().month)
col1, col2 = st.columns(2)

with col1:
    cr_now, cr_target, shortage_cr_str, _ = get_metric_data(df_cr, df_target_cr, "CR", segmen, month_column)
    metric_cr_cyc("Collection Ratio", cr_now, cr_target, shortage_cr_str, "CR")

with col2:
    cyc_now, cyc_target, shortage_cyc_str, _ = get_metric_data(df_cyc, df_target_cyc, "CYC", segmen, month_column)
    metric_cr_cyc("Current Year Collection", cyc_now, cyc_target, shortage_cyc_str, "CYC")

latest_date = df_cr['tanggal'].values[0]
st.info(f"**Terakhir diperbarui:** {latest_date}")

st.divider()


############################################################## UTIP
st.header("UTIP")
data_utip = {
    "Periode UTIP": [
        "Corrective cut off Juni 2025",
        "Progressive Juli 2025",
        "Progressive Agustus 2025",
        "Progressive September 2025",
        "Progressive Oktober 2025",
        "Progressive November 2025",
        "Progressive Desember 2025",
        "Progressive Januari 2026",
        "Progressive Februari 2026",
        "Progressive Maret 2026",
        "GRAND TOTAL",
    ],
    "Total Saldo": [
        15000000,
        12000000,
        18000000,
        11000000,
        13000000,
        14000000,
        12500000,
        16000000,
        15500000,
        17000000,
        144000000,
    ],
}
df_utip = pd.DataFrame(data_utip)

st.dataframe(df_utip)

st.divider()
#


"""
1. load database
2. filter tanggal from  17 
3. count cr
4. display target
5. count prognosa
6. display customer from highest saldo akhir

"""

df_nonpots = load_database_nonpots()
# df_nonpots = filter_column(df_nonpots, "2026-04-17")
df_nonpots["tanggal"] = pd.to_datetime(df_nonpots["tanggal"])

df_nonpots = df_nonpots[df_nonpots["tanggal"] >= "2026-04-20"]
df_nonpots = df_nonpots[df_nonpots["saldo_akhir"] > 0]

st.dataframe(df_nonpots.dtypes)

pivot_cr = df_nonpots.pivot_table(
    index=["segmen"],
    values=["saldo_akhir", "Cash", "Total Billing", "Bill BJT", "Cash BJT"],
    aggfunc="sum",
)

st.dataframe(pivot_cr)
