import numpy as np

from core.rule import BATAS_KUADRAN


def prepare_kuadran_data(df, segmen, columns_kuadran):
    from services.filters import filter_collection_data

    latest_date = df["tanggal"].max()

    df = filter_collection_data(df, segmen, tanggal=latest_date)

    df = df[columns_kuadran]

    total_pelanggan = len(df)
    total_saldo = df["saldo_akhir"].sum()

    return df, total_pelanggan, total_saldo


def prepare_data_utip(df, columns):
    df = df[columns]

    total_pelanggan = len(df)
    total_saldo = df["saldo_akhir"].sum()

    return df, total_pelanggan, total_saldo


import numpy as np
import pandas as pd

from core.rule import BATAS_KUADRAN


def assign_kuadran(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # default value
    df["kuadran"] = None

    for segmen, rule in BATAS_KUADRAN.items():

        batas_lama = rule["lama_tunggakan"]
        batas_saldo = rule["saldo_akhir"]

        mask = df["segmen"] == segmen

        saldo = df["saldo_akhir"]
        tunggakan = df["lama_tunggakan"]

        condlist = [
            saldo <= 0,
            (tunggakan <= batas_lama) & (saldo > batas_saldo),
            (tunggakan > batas_lama) & (saldo > batas_saldo),
            (tunggakan <= batas_lama) & (saldo <= batas_saldo),
            (tunggakan > batas_lama) & (saldo <= batas_saldo),
        ]

        choicelist = [0, 1, 2, 3, 4]

        df.loc[mask, "kuadran"] = np.select(condlist, choicelist, default=None)[mask]

    return df
