import streamlit as st
import pandas as pd

from core.config import SPREADSHEET_ID, WORKSHEETS
from data.spreadsheet import read_worksheet
from data.supabase import get_supabase_client
from utils.parser import parse_dataframe


@st.cache_data(ttl=600)
def load_database_nonpots():
    """Load NonPots data from Supabase (mybrains + pelanggan + keterangan)"""
    client = get_supabase_client()
    try:
        df = pd.DataFrame(client.table("mybrains_nonpots").select("*").execute().data)
        df_pelanggan = pd.DataFrame(client.table("pelanggan_nonpots").select("idnumber, nama_am, nama_akun").execute().data)
        df_keterangan = pd.DataFrame(client.table("keterangan_nonpots").select("*").execute().data)
        
        if not df_keterangan.empty and "idnumber" in df_keterangan.columns and "last_update_ket" in df_keterangan.columns:
            df_keterangan = df_keterangan.sort_values("last_update_ket", ascending=False).drop_duplicates(subset=["idnumber"], keep="first")
        
        df = df.merge(df_pelanggan, on="idnumber", how="left").merge(df_keterangan, on="idnumber", how="left")
        return df
    except Exception as e:
        st.error(f"❌ Error membaca NonPots data dari Supabase: {e}")
        return pd.DataFrame()


def load_database_cr():
    return load_database(SPREADSHEET_ID["nonpots"], "cr")


@st.cache_data(ttl=600)
def load_database_utip():
    """Load UTIP data from Supabase (utip_jtb) with nama_am merge (ACCTNO→idnumber)"""
    client = get_supabase_client()
    try:
        df_utip = pd.DataFrame(client.table("utip_jtb").select("*").execute().data)
        
        if "SALDO AKHIR" in df_utip.columns:
            df_utip = df_utip.rename(columns={"SALDO AKHIR": "saldo_akhir"})
        
        if "ACCTNO" in df_utip.columns:
            df_utip["ACCTNO"] = pd.to_numeric(df_utip["ACCTNO"], errors="coerce").astype("Int64")
        
        try:
            df_pelanggan = pd.DataFrame(client.table("pelanggan_nonpots").select("idnumber, nama_am").execute().data)
            if not df_pelanggan.empty and "ACCTNO" in df_utip.columns:
                df_utip = df_utip.merge(df_pelanggan, left_on="ACCTNO", right_on="idnumber", how="left")
                df_utip = df_utip.drop(columns=["idnumber"], errors="ignore")
        except Exception as e:
            st.warning(f"⚠️ Tidak bisa merge dengan pelanggan_nonpots: {e}")
        
        df_utip["nama_am"] = df_utip.get("nama_am", "Unknown").fillna("Unknown")
        if "kuadran" not in df_utip.columns:
            df_utip["kuadran"] = 0
        
        return df_utip
    except Exception as e:
        st.error(f"❌ Error membaca data UTIP dari Supabase: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=600)
def load_database(
    spreadsheet_key, database_name, columns: list[str] | str | None = None
):
    df = read_worksheet(spreadsheet_key, WORKSHEETS[database_name])
    df = parse_dataframe(df, database_name)
    if columns is None:
        return df
    return df[columns]
