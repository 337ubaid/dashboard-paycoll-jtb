REQUIRED_COLUMNS_MYBRAINS = {
    "idnumber": "id",
    "saldo_akhir": "currency",
    "0-3_bln": "currency",
    "4-6_bln": "currency",
    "7-12_bln": "currency",
    "13-24_bln": "currency",
    ">_24_bln": "currency",
}

SCHEMA_DATABASE_PELANGGAN = {
    "idnumber": "int",
    "nama_akun": "str",
    "nama_am": "str",
    "alamat": "str",
    "witel": "str",
    "bussiness share": "str",
    "divisi": "str",
    "segmen_2": "str",
}

SCHEMA_DATABASE_NONPOTS = {
    **REQUIRED_COLUMNS_MYBRAINS,
    "segmen": "str",
    "tanggal": "date",
    "lama_tunggakan": "int",
    "kuadran": "int",
}

SCHEMA_DATABASE_UTIP = {
    "NO": "id",
    "PAYMENT-ID": "str",
    "WITEL": "str",
    "SEGMEN": "str",
    "DATE": "date",
    "MONTH": "int",
    "YEAR": "int",
    "Periode UTIP": "str",
    "REFERENCE": "str",
    "TYPE": "str",
    "VA": "str",
    "REGEX": "str",
    "ACCTNO": "int",
    "STANDART CUSTOMER NAME": "str",
    "CURR": "str",
    "SALDO AWAL": "currency",
    "FLAG 202603": "currency",
    "PPH": "currency",
    "TAK TERIMA": "currency",
    "TAK KIRIM": "currency",
    "ADM BANK": "currency",
    "REKLAS TSEL": "currency",
    "REFUND": "currency",
    "PEND. LAIN-LAIN": "currency",
    "ADJUSTMENT": "currency",
    "SALDO AKHIR": "currency",
    "ENTRY DATE": "date",
    "KET": "str",
    "KET 2": "str",
    "STATUS AWAL": "str",
    "Agging (Bln)": "int",
    "LABEL": "str",
    "Penyelesaian": "str",
}

SCHEMA_MAP = {
    "collection": SCHEMA_DATABASE_NONPOTS,
    "pelanggan": SCHEMA_DATABASE_PELANGGAN,
    "utip": SCHEMA_DATABASE_UTIP,
}

ALL_SCHEMAS = {
    **SCHEMA_DATABASE_NONPOTS,
    **SCHEMA_DATABASE_UTIP,
    **SCHEMA_DATABASE_PELANGGAN,
}

SEGMEN = ["-Semua-", "DGS", "DPS", "DSS", "RBS", "UNIDENTIFIED"]
