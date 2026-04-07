def normalize_columns_name(df):
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def sort_values(df, sort_column="saldo_akhir"):
    df = df.sort_values(sort_column, ascending=False)
    return df


def reset_index(df):

    df = df.reset_index(drop=True)

    df.index += 1
    return df


import pandas as pd

from core.schema import REQUIRED_COLUMNS_MYBRAINS, SCHEMA_DATABASE_NONPOTS
from data.excel import load_mybrains_excel
from modules.transform import add_metadata, assign_kuadran, compute_lama_tunggakan
from utils.dataframe_utils import normalize_columns_name


def convert_excel_mybrains_nonpots(file, segmen_target, tanggal):

    df = load_mybrains_excel(file)
    df = normalize_columns_name(df)
    df = df.reindex(columns=REQUIRED_COLUMNS_MYBRAINS.keys()).copy()

    # tambahkan kolom pendukung(segmen, tanggal, kuadran)
    df = add_metadata(df, segmen_target, tanggal)
    df = compute_lama_tunggakan(df)
    df = assign_kuadran(df)

    return df


def create_empty_df():
    cols = SCHEMA_DATABASE_NONPOTS.keys()

    df = pd.DataFrame([{col: "" for col in cols}] * 11)
    return df
