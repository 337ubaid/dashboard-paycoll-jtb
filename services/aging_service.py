import numpy as np

from core.rule import AGING_RULE


def compute_lama_tunggakan(df):

    conditions = [df[col] > 0 for col in AGING_RULE.keys()]
    values = list(AGING_RULE.values())

    df["lama_tunggakan"] = np.select(conditions, values, default=0)

    return df
