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

SEGMEN = ["-Semua-", "DGS", "DPS", "DSS", "RBS"]
BULAN = {
        0: "-Semua-",
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

AGING_RULE = {
    ">_24_bln": 25,
    "13-24_bln": 24,
    "7-12_bln": 12,
    "4-6_bln": 6,
    "0-3_bln": 3,
}

BATAS_KUADRAN = {

    "RBS": {
        "lama_tunggakan": 3,
        "saldo_akhir": 10_000_000
    },

    "DGS": {
        "lama_tunggakan": 6,
        "saldo_akhir": 20_000_000
    },

    "DPS": {
        "lama_tunggakan": 6,
        "saldo_akhir": 10_000_000
    },

    "DSS": {
        "lama_tunggakan": 6,
        "saldo_akhir": 50_000_000
    }
}