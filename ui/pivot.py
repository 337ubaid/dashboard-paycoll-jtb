def pivot_am_keterangan(df, value_type="customer"):
    if value_type == "customer":
        value = "ACCTNO"
        aggfunc = "nunique"
    elif value_type == "saldo":
        value = "SALDO AKHIR"
        aggfunc = "sum"

    pivot = df.pivot_table(
        index="AM", columns="KET 2", values=value, aggfunc=aggfunc, fill_value=0
    )

    return pivot.reset_index()
