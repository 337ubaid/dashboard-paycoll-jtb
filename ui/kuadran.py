# ui/kuadran.py
import streamlit as st

from core.rule import KUADRAN_INFO, KUADRAN_KET
from ui.layout import render_dataframe
from utils.formatter import format_skala_rupiah


def render_all_kuadran(df, total_pelanggan, total_saldo):
    """Render all 4 kuadrans in a 2x2 grid."""
    c1, c2 = st.columns(2)
    with c1:
        render_kuadran(df, 1, total_pelanggan, total_saldo)
    with c2:
        render_kuadran(df, 2, total_pelanggan, total_saldo)

    c3, c4 = st.columns(2)
    with c3:
        render_kuadran(df, 3, total_pelanggan, total_saldo)
    with c4:
        render_kuadran(df, 4, total_pelanggan, total_saldo)
    st.markdown(
        "> _Kuadran membantu tim menentukan prioritas penagihan secara cepat dan objektif berdasarkan tingkat risiko._",
        text_alignment="center",
    )


def help_kuadran(kuadran):
    return KUADRAN_KET[kuadran]


def render_kuadran(df, kuadran, total_pelanggan, total_saldo):
    """Render single kuadran with customer count, saldo, and top 3 data."""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(
            f"Kuadran {kuadran}",
            help=help_kuadran(kuadran),
        )
    with col2:
        render_kuadran_legend(kuadran)

    df_display = df[df["kuadran"] == kuadran]

    # Calculate metrics
    total_pelanggan_k = len(df_display)
    total_saldo_k = df_display["saldo_akhir"].sum()

    persen_pelanggan = (
        (total_pelanggan_k / total_pelanggan * 100) if total_pelanggan else 0
    )
    persen_saldo = (total_saldo_k / total_saldo * 100) if total_saldo else 0
    saldo = format_skala_rupiah(total_saldo_k)

    # Display metrics
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"Total Pelanggan : {total_pelanggan_k} ({persen_pelanggan:.2f}%)")
    with c2:
        st.write(f"Total Saldo : {saldo} ({persen_saldo:.2f}%)")

    # Show top 3 data
    _render_top_data(df_display, "saldo_akhir")


def render_kuadran_utip(df, kuadran, total_pelanggan, total_saldo):
    """Render kuadran for UTIP data (uses SALDO AKHIR column)."""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Kuadran {kuadran}")
    with col2:
        render_kuadran_legend(kuadran)

    df_display = df[df["kuadran"] == kuadran]

    # Calculate metrics
    total_pelanggan_k = len(df_display)
    total_saldo_k = df_display["saldo_akhir"].sum()

    persen_pelanggan = (
        (total_pelanggan_k / total_pelanggan * 100) if total_pelanggan else 0
    )
    persen_saldo = (total_saldo_k / total_saldo * 100) if total_saldo else 0
    saldo = format_skala_rupiah(total_saldo_k)

    # Display metrics
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"Total Pelanggan : {total_pelanggan_k} ({persen_pelanggan:.2f}%)")
    with c2:
        st.write(f"Total Saldo : {saldo} ({persen_saldo:.2f}%)")

    # Show top 3 data
    _render_top_data_utip(df_display)


def render_kuadran_legend(kuadran):
    """Render legend for kuadran based on KUADRAN_INFO."""
    info = KUADRAN_INFO[kuadran]
    text = info["label"]
    ui_type = info["ui"]
    getattr(st, ui_type)(text)


def _render_top_data(df, sort_column):
    """Render top 3 data sorted by column."""
    df_sorted = df.sort_values(sort_column, ascending=False).reset_index(drop=True)
    df_sorted.index = df_sorted.index + 1
    render_dataframe(df_sorted.head(3).drop(columns=["kuadran"]))


def _render_top_data_utip(df):
    """Render top 3 data for UTIP."""
    df_sorted = df.sort_values("saldo_akhir", ascending=False).reset_index(drop=True)
    df_sorted.index = df_sorted.index + 1
    render_dataframe(df_sorted.head(3))
