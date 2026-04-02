import streamlit as st

from utils.dataframe_utils import reset_index


def filter_collection_data(df, segmen, kuadran=None, tanggal=None):

    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]

    if segmen != "-Semua-" or segmen is None:
        df = df[df["segmen"] == segmen]

    if kuadran is not None:
        df = df[df["kuadran"] == kuadran]

    if tanggal is not None:
        df = df[df["tanggal"] == tanggal]

    reset_index(df)

    return df


def filter_utip_data(df, segmen):
    if segmen != "-Semua-":
        df = df[df["SEGMEN"] == segmen]

    # reset_index(df)

    return df


def filter_column(df, column):
    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]
    pass
