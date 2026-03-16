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

COLUMNS_KUADRAN_UTIP = [
    "PAYMENT-ID",
    "SEGMEN",
    "ACCTNO",
    "AM",
    "SALDO AKHIR",
    "KET",
    "KET 2",
    "kuadran",
]

COLUMNS_TUNGGAKAN_AM = [
    "idnumber",
    "segmen",
    "nama_akun",
    "saldo_akhir",
    "nama_am",
    "0-3_bln",
    "4-6_bln",
    "7-12_bln",
    "13-24_bln",
    ">_24_bln",
    "lama_tunggakan",
    "kuadran",
]
