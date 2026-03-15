AGING_RULE = {
    ">_24_bln": 25,
    "13-24_bln": 24,
    "7-12_bln": 12,
    "4-6_bln": 6,
    "0-3_bln": 3,
}

BATAS_KUADRAN = {
    "RBS": {"lama_tunggakan": 3, "saldo_akhir": 10_000_000},
    "DGS": {"lama_tunggakan": 6, "saldo_akhir": 20_000_000},
    "DPS": {"lama_tunggakan": 3, "saldo_akhir": 10_000_000},  # 3
    "DSS": {"lama_tunggakan": 3, "saldo_akhir": 10_000_000},  # 3  # 10_000_000
}


KUADRAN_INFO = {
    1: {
        "label": "[ Tunggakan **BARU** -- Nominal **BESAR** ]",
        "ui": "warning",
    },
    2: {
        "label": "[ Tunggakan **LAMA** -- Nominal **BESAR** ]",
        "ui": "error",
    },
    3: {
        "label": "[ Tunggakan **BARU** -- Nominal **KECIL** ]",
        "ui": "success",
    },
    4: {
        "label": "[ Tunggakan **LAMA** -- Nominal **KECIL** ]",
        "ui": "error",
    },
}
