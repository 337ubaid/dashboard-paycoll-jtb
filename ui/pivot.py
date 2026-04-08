def pivot_am_keterangan(df, value_type="saldo"):
    if value_type == "customer":
        value = "ACCTNO"
        aggfunc = "nunique"
    elif value_type == "saldo":
        value = "SALDO AKHIR"
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
