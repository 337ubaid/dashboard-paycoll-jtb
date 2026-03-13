def normalize_columns(df):
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def reset_index(df):
    df = df.sort_values("saldo_akhir", ascending=False)

    df = df.reset_index(drop=True)

    df.index += 1
    return df
