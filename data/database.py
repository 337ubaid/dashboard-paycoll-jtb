import streamlit as st
import pandas as pd

from core.config import SPREADSHEET_ID, WORKSHEETS
from data.spreadsheet import read_worksheet
from data.supabase import get_supabase_client
from utils.parser import parse_dataframe


@st.cache_data(ttl=600)
def load_database_nonpots():
    """
    Load NonPots data from Supabase with merge
    Merge: mybrains_nonpots + pelanggan_nonpots + keterangan_nonpots
    """
    client = get_supabase_client()
    
    try:
        # Fetch mybrains_nonpots data
        response_mybrains = client.table("mybrains_nonpots").select("*").execute()
        df_collection = pd.DataFrame(response_mybrains.data)
        
        # Fetch pelanggan_nonpots data
        response_pelanggan = client.table("pelanggan_nonpots").select("idnumber, nama_am, nama_akun").execute()
        df_pelanggan = pd.DataFrame(response_pelanggan.data)
        
        # Fetch keterangan_nonpots data (latest only)
        response_keterangan = client.table("keterangan_nonpots").select("*").execute()
        df_keterangan = pd.DataFrame(response_keterangan.data)
        
        # Keep only latest keterangan per idnumber
        if not df_keterangan.empty and "idnumber" in df_keterangan.columns:
            if "last_update_ket" in df_keterangan.columns:
                df_keterangan = df_keterangan.sort_values("last_update_ket", ascending=False)
                df_keterangan = df_keterangan.drop_duplicates(subset=["idnumber"], keep="first")
        
        # Merge: collection + pelanggan (by idnumber)
        df = df_collection.merge(df_pelanggan, on="idnumber", how="left")
        
        # Merge: + keterangan (by idnumber)
        df = df.merge(df_keterangan, on="idnumber", how="left")
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error membaca NonPots data dari Supabase: {e}")
        return pd.DataFrame()


#
def load_database_cr():
    df = load_database(SPREADSHEET_ID["nonpots"], "cr")
    return df


# #


@st.cache_data(ttl=600)
def load_database_utip():
    """
    Load UTIP data from Supabase table 'utip_jtb'
    Merge dengan tabel pelanggan untuk mendapatkan nama_am
    
    Note: ACCTNO (text) needs to convert to int64 to match idnumber (bigint)
    """
    client = get_supabase_client()
    
    try:
        # Fetch UTIP data from utip_jtb table
        response_utip = client.table("utip_jtb").select("*").execute()
        df_utip = pd.DataFrame(response_utip.data)
        
        # Standardize column names - rename SALDO AKHIR to saldo_akhir
        if "SALDO AKHIR" in df_utip.columns:
            df_utip = df_utip.rename(columns={"SALDO AKHIR": "saldo_akhir"})
        
        # Convert ACCTNO to int64 untuk merge dengan idnumber
        if "ACCTNO" in df_utip.columns:
            try:
                df_utip["ACCTNO"] = pd.to_numeric(df_utip["ACCTNO"], errors="coerce").astype("Int64")
            except Exception as e:
                st.warning(f"⚠️ Warning converting ACCTNO to numeric: {e}")
        
        # Fetch pelanggan data untuk mendapatkan nama_am
        try:
            response_pelanggan = client.table("pelanggan_nonpots").select("idnumber, nama_am").execute()
            df_pelanggan = pd.DataFrame(response_pelanggan.data)
            
            # Merge dengan pelanggan data berdasarkan ACCTNO = idnumber
            if df_pelanggan is not None and not df_pelanggan.empty and "ACCTNO" in df_utip.columns:
                df_utip = df_utip.merge(
                    df_pelanggan, 
                    left_on="ACCTNO", 
                    right_on="idnumber", 
                    how="left"
                )
                # Drop duplicate idnumber column dari merge
                if "idnumber" in df_utip.columns:
                    df_utip = df_utip.drop(columns=["idnumber"])
        except Exception as e:
            st.warning(f"⚠️ Tidak bisa merge dengan pelanggan_nonpots: {e}")
        
        # Add default values jika kolom masih tidak ada
        if "nama_am" not in df_utip.columns:
            df_utip["nama_am"] = "Unknown"
        else:
            # Fill NaN values dengan "Unknown"
            df_utip["nama_am"] = df_utip["nama_am"].fillna("Unknown")
        
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
