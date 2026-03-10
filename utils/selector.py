import streamlit as st
from datetime import datetime
from utils.schema import BULAN, SEGMEN

def pilih_kategori():
    """
    Komponen UI untuk memilih Segmen, Bulan, dan Tahun.

    Fungsi ini menampilkan 3 buah dropdown (Streamlit selectbox):
    1. **Segmen**: pilihan segmen bisnis (misalnya DGS, DPS, DSS, RBS, atau semua).
    2. **Bulan** : pilihan bulan (Januari–Desember atau "-Semua-").
    3. **Tahun** : pilihan tahun (tahun sekarang dan tahun sebelumnya).

    Returns
    -------
    tuple
        (bulan_target: int, tahun_target: int, segmen_target: str)
        - `bulan_target` : nomor bulan (1–12) atau `0` untuk "-Semua-"
        - `tahun_target` : tahun dalam format integer (mis. 2025)
        - `segmen_target`: string segmen yang dipilih
    """
    col1, col2, col3 = st.columns(3)

    # Pilihan segmen
    segmen_target = col1.selectbox(
        "Pilih Segmen",
        SEGMEN
    )

    # Pilihan bulan
    bulan_target = col2.selectbox(
        "Pilih Bulan",
        list(BULAN.keys()),
        format_func=lambda x: BULAN[x]
    )
        # Pilihan tahun (hanya tahun sekarang & tahun sebelumnya)
    tahun_sekarang = datetime.now().year
    tahun_target = col3.selectbox(
        "Pilih Tahun",
        [tahun_sekarang, tahun_sekarang - 1]
    )

    return bulan_target, tahun_target, segmen_target