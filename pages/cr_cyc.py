from datetime import datetime

import pandas as pd
import streamlit as st

from data.supabase import get_database_cr_cyc
from ui.layout import setup_page
from utils.selector import pilih_all_segmen

# Constants
SCALE_FACTOR = 1_000_000_000  # For shortage calculation (data in Billions)


def render_metric_header(label: str, now: float, target: float, shortage: str, metric_prefix: str = "CR"):
    """Render a section header with metrics for CR or CYC."""
    st.header(label)
    col1, col2 = st.columns(2)
    
    delta = now - target
    col1.metric(
        label=f"Total {metric_prefix}",
        value=f"{now:.2%}",
        delta=f"{delta:.2%}",
        delta_arrow="off"
    )
    col2.metric(label=f"Target {metric_prefix}", value=f"{target:.2%}")
    st.metric("Shortage", shortage)


def calculate_shortage(diff: float, bill_total: float, bill_bjt: float, cash_bjt: float) -> float:
    """Calculate the shortage amount based on difference from target."""
    return diff * (bill_total - bill_bjt + cash_bjt) * -SCALE_FACTOR


def get_metric_values(df: pd.DataFrame, df_target: pd.DataFrame, metric_type: str, segmen: str, month: str):
    """Extract and calculate metric data from dataframes."""
    # Column mapping based on metric type
    value_col = "CYC CASH" if metric_type == "CYC" else "CR CASH"
    bill_col = "BILL" if metric_type == "CYC" else "BILL (TOTAL)"
    
    # Filter by segment
    row = df[df['UBIS'] == segmen]
    target_row = df_target[df_target['SEGMEN'] == segmen]
    
    if row.empty:
        return 0.0, 0.0, "Rp 0", 0.0
        
    now = row[value_col].values[0]
    target = target_row[month].values[0] if not target_row.empty and month in target_row.columns else 0.0
    
    bill_total = row[bill_col].values[0]
    bill_bjt = row['BILL BJT'].values[0]
    cash_bjt = row['CASH BJT'].values[0]
    
    diff = target - now
    shortage = calculate_shortage(diff, bill_total, bill_bjt, cash_bjt)
    
    return now, target, f"Rp {shortage:,.0f}", shortage


# Page Setup
setup_page("CR CYC Performance", "🗓️")

# Sidebar Filter
selected_segmen = pilih_all_segmen() or "Total"

# Data Fetching
df_cr, df_target_cr, df_cyc, df_target_cyc = get_database_cr_cyc(selected_segmen)

# Metric Rendering
current_month = str(datetime.now().month)
col1, col2 = st.columns(2)

with col1:
    cr_now, cr_target, cr_shortage_str, _ = get_metric_values(
        df_cr, df_target_cr, "CR", selected_segmen, current_month
    )
    render_metric_header("Collection Ratio", cr_now, cr_target, cr_shortage_str, "CR")

with col2:
    cyc_now, cyc_target, cyc_shortage_str, _ = get_metric_values(
        df_cyc, df_target_cyc, "CYC", selected_segmen, current_month
    )
    render_metric_header("Current Year Collection", cyc_now, cyc_target, cyc_shortage_str, "CYC")

# Update Info
if not df_cr.empty:
    latest_date = df_cr['tanggal'].values[0]
    st.info(f"**Terakhir diperbarui:** {latest_date}")

st.divider()
