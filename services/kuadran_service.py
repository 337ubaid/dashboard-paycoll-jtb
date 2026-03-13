import numpy as np
from core.rule import BATAS_KUADRAN


def assign_kuadran_labels(df):

    df = df.copy()

    rules = df["segmen"].map(BATAS_KUADRAN)

    lama_limit = rules.apply(lambda x: x["lama_tunggakan"])
    saldo_limit = rules.apply(lambda x: x["saldo_akhir"])

    conditions = [
        (df["saldo_akhir"] <= 0),
        (df["lama_tunggakan"] <= lama_limit) & (df["saldo_akhir"] > saldo_limit),
        (df["lama_tunggakan"] > lama_limit) & (df["saldo_akhir"] > saldo_limit),
        (df["lama_tunggakan"] <= lama_limit) & (df["saldo_akhir"] <= saldo_limit),
        (df["lama_tunggakan"] > lama_limit) & (df["saldo_akhir"] <= saldo_limit),
    ]

    choices = [0, 1, 2, 3, 4]

    df["kuadran"] = np.select(conditions, choices)

    return df
