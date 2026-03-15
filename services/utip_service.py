def agg_keterangan(df, col_ket="KET 2", value_type="customer"):

    if value_type == "customer":
        data = df.groupby(col_ket)["ACCTNO"].nunique()

    elif value_type == "saldo":
        data = df.groupby(col_ket)["SALDO AKHIR"].sum()

    return data.reset_index(name="value")
