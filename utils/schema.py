# need to remove
REQUIRED_COLUMNS_MYBRAINS = [
    "idnumber",
    "saldo_akhir",
    "0-3_bln",
    "4-6_bln",
    "7-12_bln",
    "13-24_bln",
    ">_24_bln",
]

COLUMN_TYPES_MYBRAIN = {
    "idnumber": int,
    "saldo_akhir": int,
    "0-3_bln": int,
    "4-6_bln": int,
    "7-12_bln": int,
    "13-24_bln": int,
    ">_24_bln": int,
}
SEGMEN = ["-Semua-", "DGS", "DPS", "DSS", "RBS", "UNIDENTIFIED"]
