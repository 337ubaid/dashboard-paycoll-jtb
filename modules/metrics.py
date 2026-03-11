import pandas as pd
import streamlit as st
from utils.date_utils import get_reference_dates


def filter_data(df, segmen):

    if segmen != "ALL":
        df = df[df["segmen"] == segmen]

    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]

    return df


def get_value_by_date(df, target_date):

    df_day = df[df["billper"] == target_date]

    if df_day.empty:
        return 0

    return df_day["saldo_akhir"].sum()


def compute_metrics(df, segmen):

    today, yesterday, day6 = get_reference_dates()

    df = filter_data(df, segmen)

    val_today = get_value_by_date(df, today)
    val_yesterday = get_value_by_date(df, yesterday)
    val_day6 = get_value_by_date(df, day6)
    
    # st.write(val_today)

    return df, {
        "today": val_today,
        "delta_yesterday": val_today - val_yesterday,
        "delta_day6": val_today - val_day6,
        "day6": val_day6
    }