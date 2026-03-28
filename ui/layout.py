import streamlit as st

from utils.formatter import format_currency, format_headers


def render_sidebar():
    """
    Fungsi untuk menampilkan menu di sidebar.
    """

    with st.sidebar:
        st.title("Menu")
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link(
            "pages/update_mybrains_nonpots.py",
            label="Update Daily",
            icon=":material/event_repeat:",
        )
        st.page_link("pages/kuadran.py", label="Kuadran", icon=":material/dataset:")
        st.page_link(
            "pages/update_batas_kuadran.py",
            label="Batas Kuadran",
            icon=":material/dataset:",
        )
        st.page_link("pages/utip.py", label="UTIP", icon=":material/money_bag:")


def print_sort_dataframe(df):
    df = df.sort_values("saldo_akhir", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    render_dataframe(df)


def render_dataframe(df):
    header_map = format_headers(df)
    df = format_currency(df)
    st.dataframe(df, column_config=header_map)


from core.rule import KUADRAN_INFO
from utils.formatter import format_skala_rupiah


def render_all_kuadran(df, total_pelanggan, total_saldo):
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


def render_kuadran(df, kuadran, total_pelanggan, total_saldo):
    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:
        st.subheader(f"Kuadran {kuadran}")
    with col2:
        render_kuadran_legend(kuadran)
    df_display = df[df["kuadran"] == kuadran]

    total_pelanggan_k = len(df_display)
    total_saldo_k = df_display["saldo_akhir"].sum()

    persen_pelanggan = (
        (total_pelanggan_k / total_pelanggan * 100) if total_pelanggan else 0
    )
    persen_saldo = (total_saldo_k / total_saldo * 100) if total_saldo else 0

    saldo = format_skala_rupiah(total_saldo_k)

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"Total Pelanggan : {total_pelanggan_k} ({persen_pelanggan:.2f}%)")

    with c2:
        st.write(f"Total Saldo : {saldo} ({persen_saldo:.2f}%)")

    print_sort_dataframe(df_display.head(3))


def render_kuadran_utip(df, kuadran, total_pelanggan, total_saldo):
    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:
        st.subheader(f"Kuadran {kuadran}")
    with col2:
        render_kuadran_legend(kuadran)
    df_display = df[df["kuadran"] == kuadran]

    total_pelanggan_k = len(df_display)
    total_saldo_k = df_display["SALDO AKHIR"].sum()

    persen_pelanggan = (
        (total_pelanggan_k / total_pelanggan * 100) if total_pelanggan else 0
    )
    persen_saldo = (total_saldo_k / total_saldo * 100) if total_saldo else 0

    saldo = format_skala_rupiah(total_saldo_k)

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"Total Pelanggan : {total_pelanggan_k} ({persen_pelanggan:.2f}%)")

    with c2:
        st.write(f"Total Saldo : {saldo} ({persen_saldo:.2f}%)")

    df_display = df_display.sort_values("SALDO AKHIR", ascending=False)
    df_display = df_display.reset_index(drop=True)
    df_display.index = df_display.index + 1
    render_dataframe(df_display.head(3))


def render_kuadran_legend(kuadran):

    info = KUADRAN_INFO[kuadran]

    text = info["label"]
    ui_type = info["ui"]

    getattr(st, ui_type)(text)
