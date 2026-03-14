from datetime import date, timedelta

TODAY = date.today()

COLUMNS_KUADRAN = [
    "idnumber",
    "nama_akun",
    "segmen",
    "nama_am",
    "saldo_akhir",
    "kuadran",
]

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
