def filter_collection_data(df, segmen, kuadran=None, tanggal=None):

    df = df[(df["saldo_akhir"] > 0) | (df["kuadran"] != 0)]

    if segmen != "-Semua-":
        df = df[df["segmen"] == segmen]

    if kuadran is not None:
        df = df[df["kuadran"] == kuadran]

    if tanggal is not None:
        df = df[df["tanggal"] == tanggal]

    df = df.sort_values("saldo_akhir", ascending=False)

    df = df.reset_index(drop=True)

    df.index += 1

    return df
