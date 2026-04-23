import pandas as pd
import streamlit as st

from data.database import load_database_nonpots
from services.filters import filter_column
from ui.layout import setup_page

setup_page("CR CYC Performance", "🗓️")


def metric_cr_cyc(cr_cyc, now, target, shortage):

    st.header(cr_cyc)
    c1, c2 = st.columns(2)

    c1.metric(
        "Total CR",
        f"{now:.2f}%",
        delta=f"{target - now:.2f}%",
    )
    c2.metric(
        "Target CR",
        f"{target:.2f}%",
    )
    st.metric(
        "Shortage",
        shortage,
    )


def count_shortage(diff_cr, bill_total, bill_bjt, cash_bjt):
    return diff_cr * (bill_total - bill_bjt + cash_bjt)


col1, col2 = st.columns(2)
#
cr_now = 95.95
cr_target = 99.00

diff_cr = cr_target - cr_now
bill_total = 14_273_704
bill_bjt = 142_704
cash_bjt = 142_704


shortage = count_shortage(diff_cr, bill_total, bill_bjt, cash_bjt)

with col1:
    metric_cr_cyc(
        "Collection Ratio",
        cr_now,
        cr_target,
        f"Rp {shortage:,.2f}",
    )

with col2:
    metric_cr_cyc(
        "Current Year Collection",
        cr_now,
        cr_target,
        shortage,
    )
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
