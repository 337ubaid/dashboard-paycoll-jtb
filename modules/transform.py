import numpy as np
import streamlit as st
from utils.schema import AGING_RULE
from utils.schema import BATAS_KUADRAN

def add_metadata(df, segmen, billper):

    df = df.copy()

    df["segmen"] = segmen
    df["billper"] = billper

    return df


def compute_lama_tunggakan(df):

    conditions = [df[col] > 0 for col in AGING_RULE.keys()]
    values = list(AGING_RULE.values())

    df["lama_tunggakan"] = np.select(
        conditions,
        values,
        default=0
    )

    return df


def compute_kuadran(row):

    segmen = row["segmen"]

    rule = BATAS_KUADRAN.get(segmen)

    # st.write(segmen)
    # st.write(rule)

    if row["saldo_akhir"] <= 0:
        return 0
    
    if row["lama_tunggakan"] <= rule["lama_tunggakan"] and row["saldo_akhir"] > rule["saldo_akhir"]:
        return 1

    if row["lama_tunggakan"] > rule["lama_tunggakan"] and row["saldo_akhir"] > rule["saldo_akhir"]:
        return 2

    if row["lama_tunggakan"] <= rule["lama_tunggakan"] and row["saldo_akhir"] <= rule["saldo_akhir"]:
        return 3
    
    if row["lama_tunggakan"] > rule["lama_tunggakan"] and row["saldo_akhir"] <= rule["saldo_akhir"]:
        return 4

    
def assign_kuadran(df):
    df["kuadran"] = df.apply(compute_kuadran, axis=1)
    return df