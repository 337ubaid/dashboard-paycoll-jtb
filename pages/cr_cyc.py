import pandas as pd
import streamlit as st
from datetime import datetime

from data.database import load_database_cr, load_database_nonpots
from services.filters import filter_column
from ui.layout import setup_page
from utils.selector import pilih_segmen

setup_page("CR CYC Performance", "🗓️")

segmen = pilih_segmen()

conn= st.connection("supabase")
query = """
select * from mybrains_cr
"""
df_cr = conn.query(query)
st.dataframe(df_cr)

df_target_cr = conn.query("select * from target_cr", params={"ubis": segmen})
st.write(df_target_cr)

# metric_cr_cyc
def metric_cr_cyc(cr_cyc, now, target, shortage):
    st.header(cr_cyc)
    c1, c2 = st.columns(2)


    c1.metric(
        "Total CR",
        f"{now:.2%}",
        delta=f"{now - target:.2%}",
        delta_arrow="off",
    )
    c2.metric(
        "Target CR",
        f"{target:.2%}",
    )
    st.metric(
        "Shortage",
        shortage,
    )


def count_shortage(diff_cr, bill_total, bill_bjt, cash_bjt):
    return diff_cr * (bill_total - bill_bjt + cash_bjt) * -1_000_000_000


col1, col2 = st.columns(2)

cr_now = df_cr[df_cr['UBIS'] == segmen]['CR CASH'].values[0]

current_month = datetime.now().month
month_column = str(current_month)

target_row = df_target_cr[df_target_cr['SEGMEN'] == segmen]
if not target_row.empty and month_column in target_row.columns:
    cr_target = target_row[month_column].values[0]
else:
    cr_target = 0.0

diff_cr = cr_target - cr_now
bill_total = df_cr[df_cr['UBIS'] == segmen]['BILL (TOTAL)'].values[0]
bill_bjt = df_cr[df_cr['UBIS'] == segmen]['BILL BJT'].values[0]
cash_bjt = df_cr[df_cr['UBIS'] == segmen]['CASH BJT'].values[0]


shortage = count_shortage(diff_cr, bill_total, bill_bjt, cash_bjt)

with col1:
    metric_cr_cyc(
        "Collection Ratio",
        cr_now,
        cr_target,
        f"Rp {shortage:,.0f}",
    )
    # st.header("Top 10")
with col2:
    metric_cr_cyc(
        "Current Year Collection",
        cr_now,
        cr_target,
        shortage,
    )
    # st.header("Top 10")
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
