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


def render_editable_keterangan(df, key_suffix):
    """
    Render an editable data editor for the 'keterangan' column 
    and show changes.
    """
    st.info(f"{len(df)} Pelanggan")
    
    # Configure editable columns
    df_edited = st.data_editor(
        df,
        disabled=[col for col in df.columns if col != "keterangan"],
        key=f"editor_ket_{key_suffix}",
        width="stretch"
    )

    # Detect changes
    df_original = df.fillna("")
    df_current = df_edited.fillna("")

    # Compare by idnumber
    original_ket = df_original.set_index("idnumber")["keterangan"]
    current_ket = df_current.set_index("idnumber")["keterangan"]
    
    changed_ids = original_ket.ne(current_ket)
    
    if changed_ids.any():
        changes = df_current[df_current["idnumber"].isin(changed_ids[changed_ids].index)]
        st.subheader("Perubahan Tersimpan (Preview)")
        st.write(changes[["idnumber", "nama_akun", "nama_am", "keterangan"]])


# --- Data Initialization ---
df_database = get_database_detail_pelanggan()
latest_date = df_database["tanggal"].max()

# --- Page Config ---
setup_page("Detail Pelanggan", "❇️")

# --- Filters ---
c1, c2, _ = st.columns(3)
with c1:
    segmen_target = pilih_all_segmen()
with c2:
    nama_am = input_am()

# Filter by AM Name
filtered_df = cari_am(df_database, nama_am)

if filtered_df.empty:
    am_display = nama_am if nama_am.upper().startswith("AM") else f"AM {nama_am}"
    st.error(f"{am_display.upper()} tidak ditemukan.")
    st.stop()

# --- Section: Summary ---
st.header("📌 Summary")
col_m, col_c = st.columns(2)
with col_m:
    render_dashboard_metrics(filtered_df, segmen_target)
with col_c:
    print_chart_tren_saldo(filtered_df, segmen_target)

# --- Section: Kuadran ---
st.header(
    "📌 Kuadran",
    help="Pengelompokkan prioritas pelanggan berdasarkan besar **Nilai Pinjaman** dan **Lama Tunggakan**",
)

tab_overview, tab_details = st.tabs(["Ringkasan", "Detail"])

# Filter for the latest date for Kuadran analysis
df_latest = filter_collection_data(filtered_df, segmen_target, tanggal=latest_date)

with tab_overview:
    df_kuadran, total_pelanggan, total_saldo = prepare_kuadran_data(
        df_latest, segmen_target, COLUMNS_KUADRAN
    )
    render_all_kuadran(df_kuadran, total_pelanggan, total_saldo)

with tab_details:
    st.subheader("Detail Tiap Kuadran")
    tab_labels = ["SEMUA", "Kuadran 1", "Kuadran 2", "Kuadran 3", "Kuadran 4"]
    sub_tabs = st.tabs(tab_labels)

    for i, tab in enumerate(sub_tabs):
        with tab:
            df_target = df_latest if i == 0 else df_latest[df_latest["kuadran"] == i]
            render_editable_keterangan(df_target, key_suffix=i)

# --- Section: UTIP ---
st.divider()
st.header("📌 UTIP (Uang Titipan)")
df_db_utip = load_database_utip()
filtered_df_utip = cari_am(df_db_utip, nama_am)
st.dataframe(filtered_df_utip, width="stretch")
