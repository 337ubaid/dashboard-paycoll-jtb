from utils.dataframe_utils import reset_index


def filter_collection_data(df, segmen, kuadran=None, tanggal=None):

    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]

    if segmen != "-Semua-":
        df = df[df["segmen"] == segmen]

    if kuadran is not None:
        df = df[df["kuadran"] == kuadran]

    if tanggal is not None:
        df = df[df["tanggal"] == tanggal]

    reset_index(df)

    return df
