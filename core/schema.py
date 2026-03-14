REQUIRED_COLUMNS_MYBRAINS = {
    "idnumber": "int",
    "saldo_akhir": "int",
    "0-3_bln": "int",
    "4-6_bln": "int",
    "7-12_bln": "int",
    "13-24_bln": "int",
    ">_24_bln": "int",
}

SCHEMA_DATABASE_PELANGGAN = {
    "idnumber": "int",
    "nama_akun": "str",
    "nama_am": "str",
    "ALAMAT": "str",
    "Witel": "str",
    "Bussiness Share": "str",
    "Divisi": "str",
    "Segmen": "str",
}

SCHEMA_DATABASE_NONPOTS = {
    **REQUIRED_COLUMNS_MYBRAINS,
    "segmen": "str",
    "tanggal": "date",
    "lama_tunggakan": "int",
    "kuadran": "int",
}

SCHEMA_DATABASE_UTIP = {
    "NO": "int",
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
    "SALDO AWAL": "int",
    "FLAG 202603": "int",
    "PPH": "int",
    "TAK TERIMA": "int",
    "TAK KIRIM": "int",
    "ADM BANK": "int",
    "REKLAS TSEL": "int",
    "REFUND": "int",
    "PEND. LAIN-LAIN": "int",
    "ADJUSTMENT": "int",
    "SALDO AKHIR": "int",
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

SEGMEN = ["-Semua-", "DGS", "DPS", "DSS", "RBS", "UNIDENTIFIED"]
