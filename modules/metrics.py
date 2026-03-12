import pandas as pd
import streamlit as st
from utils.date_utils import get_reference_dates

today, yesterday, day6 = get_reference_dates()

def filter_data(df, segmen, kuadran=None, tanggal=None):
    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]
    
    if segmen != "-Semua-":
        df = df[df["segmen"] == segmen]
    
    if kuadran is not None:
        df = df[df["kuadran"] == kuadran]

    if tanggal is not None:
        df = df[df["tanggal"] == tanggal]

    df = df.sort_values("saldo_akhir", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    return df


def get_saldo_by_date(df, target_date):

    df_day = df[df["tanggal"] == target_date]

    if df_day.empty:
        return 0

    return df_day["saldo_akhir"].sum()

def get_total_pelanggan_by_date(df, target_date):
    
    df_day = df[df["tanggal"] == target_date]

    return len(df_day)



def compute_metrics(df, segmen):

    df = filter_data(df, segmen)
    
    val_today = get_saldo_by_date(df, today)
    val_yesterday = get_saldo_by_date(df, yesterday)
    val_day6 = get_saldo_by_date(df, day6)
    
    pelanggan_today = get_total_pelanggan_by_date(df, today)
    pelanggan_yesterday = get_total_pelanggan_by_date(df, yesterday)
    pelanggan_day6 = get_total_pelanggan_by_date(df, day6)

    return df, {
        "today": val_today,
        "delta_yesterday": val_today - val_yesterday,
        "delta_day6": val_today - val_day6,
        "day6": val_day6
    },{
        "today": pelanggan_today,
        "delta_yesterday": pelanggan_today - pelanggan_yesterday,
        "delta_day6": pelanggan_today - pelanggan_day6,
        "day6": pelanggan_day6
        
    }

def show_metrics(df, segmen_target='-Semua-'):
    df, metrics_saldo, metrics_pelanggan = compute_metrics(df, segmen_target)
    col1, col2 = st.columns(2)
    with col1:
        ## METRIC SALDO AWAL
        st.metric(
            "Saldo Awal Bulan Ini",
            f"{metrics_saldo['day6']:,.0f}",
            f"{metrics_saldo['delta_day6']:,.0f}",
            delta_color="inverse"
        )
        ## METRIC SALDO TODAY
        st.metric(
            "Saldo Hari Ini (dibanding 3 hari lalu)",
            f"{metrics_saldo['today']:,.0f}",
            f"{metrics_saldo['delta_yesterday']:,.0f}",
            delta_color="inverse"
        )
    with col2:
        st.metric(
            "Pelanggan Awal Bulan Ini",
            f"{metrics_pelanggan['day6']:,.0f}",
            f"{metrics_pelanggan['delta_day6']:,.0f}",
            delta_color="inverse"
        )
        st.metric(
            "Pelanggan Hari Ini (dibanding 3 hari lalu)",
            f"{metrics_pelanggan['today']:,.0f}",
            f"{metrics_pelanggan['delta_yesterday']:,.0f}",
            delta_color="inverse"
        )      