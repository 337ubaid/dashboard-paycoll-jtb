def sum_saldo_by_date(df, target_date):

    df_day = df[df["tanggal"] == target_date]

    if df_day.empty:
        return 0

    return df_day["saldo_akhir"].sum()


def count_pelanggan_by_date(df, target_date):

    df_day = df[df["tanggal"] == target_date]

    return len(df_day)
