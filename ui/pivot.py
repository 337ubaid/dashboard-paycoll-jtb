def pivot_am_keterangan(df, value_type="saldo"):
    if value_type == "customer":
        value = "ACCTNO"
        aggfunc = "nunique"
    elif value_type == "saldo":
        value = "saldo_akhir"
        aggfunc = "sum"

    pivot = df.pivot_table(
        index="nama_am",
        columns="KET 2",
        values=value,
        aggfunc=aggfunc,
        fill_value=0,
        margins=True,  # menambah total
        margins_name="GRAND TOTAL",  # nama total
    )

    return pivot.reset_index()


def pivot_periode_utip(df_utip, value_type="saldo_akhir"):
    pivot = df_utip.pivot_table(
        index="Periode UTIP",
        values=value_type,
        aggfunc="sum",
        fill_value=0,
        margins=True,  # menambah total
        margins_name="GRAND TOTAL",  # nama total
    )

    return pivot.reset_index()
