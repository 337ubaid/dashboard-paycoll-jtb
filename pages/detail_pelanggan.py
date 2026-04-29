import streamlit as st

from core.constant import COLUMNS_KUADRAN
from data.database import load_database_utip
from data.supabase import get_database_detail_pelanggan
from services.filters import filter_collection_data
from services.kuadran_service import prepare_kuadran_data
from ui.chart import print_chart_tren_saldo
from ui.kuadran import render_all_kuadran
from ui.layout import setup_page
from ui.metrics import render_dashboard_metrics
from utils.selector import cari_am, input_am, pilih_all_segmen


def update_keterangan(df, key_suffix):
    df_edit_keterangan = st.data_editor(
        df,
        disabled=df.drop(columns=["keterangan"]),
        key=f"editor_ket_{key_suffix}",
    )

    df = df.fillna("")
    df_edit_keterangan = df_edit_keterangan.fillna("")

    df_ket = df.set_index("idnumber")["keterangan"]
    df_edit_keterangan_ket = df_edit_keterangan.set_index("idnumber")["keterangan"]

    changed_ids = df_ket.ne(df_edit_keterangan_ket)  # not equal

    result = df_edit_keterangan[
        df_edit_keterangan["idnumber"].isin(changed_ids[changed_ids].index)
    ]
    result = result[["idnumber", "nama_akun", "nama_am", "keterangan"]]

    st.write(result)


df_database = get_database_detail_pelanggan()
latest_date = df_database["tanggal"].max()

setup_page("Detail Pelanggan", "❇️")

c1, c2, _ = st.columns(3)
with c1:
    segmen_target = pilih_all_segmen()
with c2:
    nama_am = input_am()

filtered_df = cari_am(df_database, nama_am)

if filtered_df.empty:
    am_display = nama_am if nama_am.upper().startswith("AM") else f"AM {nama_am}"
    st.error(f"{am_display.upper()} tidak ditemukan.")
    st.stop()

st.header("📌 Summary")
c1, c2 = st.columns(2)
with c1:
    render_dashboard_metrics(filtered_df, segmen_target)
with c2:
    print_chart_tren_saldo(filtered_df, segmen_target)

st.header(
    "📌 Kuadran",
    help="Pengelompokkan prioritas pelanggan berdasarkan besar **Nilai Pinjaman** dan **Lama Tunggakan**",
)
tab_kuadran, tab_details = st.tabs(["Kuadran", "Detail"])
filtered_df = filter_collection_data(filtered_df, segmen_target, tanggal=latest_date)

with tab_kuadran:
    df_kuadran, total_pelanggan, total_saldo = prepare_kuadran_data(
        filtered_df, segmen_target, COLUMNS_KUADRAN
    )

    render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)
with tab_details:
    st.subheader("Detail Kuadran")
    tab_names = ["ALL", "Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            if i == 0:
                df_show = filtered_df
            else:
                df_show = filtered_df[filtered_df["kuadran"] == i]
            st.info(f"{len(df_show)} Pelanggan")
            update_keterangan(df_show, key_suffix=i)


st.divider()
st.header(
    "📌 UTIP",
    help="Uang Titipan",
)
df_db_utip = load_database_utip()
filtered_df_utip = cari_am(df_db_utip, nama_am)
st.dataframe(filtered_df_utip)
