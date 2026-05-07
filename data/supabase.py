from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

import pandas as pd
import streamlit as st
from supabase import create_client, Client

conn = st.connection("supabase")


@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and cache Supabase client for direct operations."""
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    return create_client(supabase_url, supabase_key)


@st.cache_data(ttl=60)
def fetch_data(query: str, where_clause: Optional[str] = None, params: Optional[dict] = None) -> pd.DataFrame:
    """Internal helper to fetch data from Supabase with caching."""
    final_query = query + (where_clause or "")
    return conn.query(final_query, params=params or {})


def build_where_clause(filters: dict, base_conditions: Optional[List[str]] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Build a SQL WHERE clause and parameters from filters and base conditions.
    """
    conditions = list(base_conditions or [])
    params = {}

    for key, value in filters.items():
        if value is not None and value != "-Semua-":
            conditions.append(f"{key} = :{key}")
            params[key] = value

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    return where_clause, params


def get_metric_tanggal() -> List[str]:
    """Get the reference dates for metrics (latest 2 and day 5/6 of month)."""
    query = """
    WITH latest_dates AS (
        SELECT DISTINCT tanggal
        FROM mybrains_nonpots
        ORDER BY tanggal DESC
        LIMIT 2
    ),
    latest_month AS (
        SELECT DATE_TRUNC('month', MAX(tanggal)) AS bulan_terbaru
        FROM mybrains_nonpots
    ),
    tanggal_enam AS (
        SELECT tanggal
        FROM mybrains_nonpots, latest_month
        WHERE tanggal = bulan_terbaru + INTERVAL '5 days'
    )
    SELECT tanggal FROM latest_dates
    UNION
    SELECT tanggal FROM tanggal_enam
    ORDER BY tanggal DESC;
    """
    df = fetch_data(query)
    return df["tanggal"].tolist()


def get_metric_saldo(filters: dict) -> pd.DataFrame:
    """Fetch metric data (saldo and count) for specific reference dates."""
    list_tanggal = get_metric_tanggal()

    filters = filters.copy()
    filters.pop("tanggal", None)

    conditions = ["saldo_akhir > 0"]
    where_clause, params = build_where_clause(filters, conditions)

    # dynamic IN clause for dates
    placeholders = []
    for i, tgl in enumerate(list_tanggal):
        key = f"tgl_{i}"
        placeholders.append(f":{key}")
        params[key] = tgl

    tanggal_clause = f"tanggal IN ({','.join(placeholders)})"
    where_clause += (f" AND {tanggal_clause}" if "WHERE" in where_clause else f" WHERE {tanggal_clause}")

    query = """
        SELECT 
            tanggal,
            SUM(saldo_akhir) as total_saldo,
            COUNT(DISTINCT idnumber) as total_pelanggan
        FROM mybrains_nonpots
    """

    query = query + where_clause + " GROUP BY tanggal ORDER BY tanggal DESC"
    return fetch_data(query, params=params)


def get_data_nonpots(filters: dict) -> pd.DataFrame:
    """Fetch all non-pots data for the latest date."""
    conditions = [
        "saldo_akhir > 0",
        "tanggal = (SELECT MAX(tanggal) FROM mybrains_nonpots)",
    ]
    where_clause, params = build_where_clause(filters, conditions)
    query = "SELECT * FROM mybrains_nonpots"
    return fetch_data(query, where_clause, params)


def get_database_detail_pelanggan() -> pd.DataFrame:
    """Fetch and merge database for Detail Pelanggan view."""
    df_mybrains = conn.query("select * from mybrains_nonpots where saldo_akhir > 0")
    df_pelanggan = conn.query("select idnumber, nama_akun, nama_am from pelanggan_nonpots")
    
    # Get only the latest keterangan for each idnumber
    latest_keterangan_query = """
        select * from keterangan_nonpots
        where (idnumber, last_update_ket) in (
            select idnumber, MAX(last_update_ket) 
            from keterangan_nonpots 
            group by idnumber
        )
    """
    df_keterangan = conn.query(latest_keterangan_query)

    df_database = df_mybrains.merge(df_pelanggan, on="idnumber", how="left")
    df_database = df_database.merge(df_keterangan, on="idnumber", how="left")

    return df_database


def get_database_cr_cyc(segmen: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Fetch all CR and CYC data for Performance view."""
    # Note: query builder could be used here too if filters are complex
    df_cr = conn.query(
        "select * from mybrains_cr where tanggal = (select MAX(tanggal) from mybrains_cr)",
        params={"ubis": segmen},
    )
    df_target_cr = conn.query("select * from target_cr", params={"ubis": segmen})
    df_cyc = conn.query(
        "select * from mybrains_cyc where tanggal = (select MAX(tanggal) from mybrains_cyc)",
        params={"ubis": segmen},
    )
    df_target_cyc = conn.query("select * from target_cyc", params={"ubis": segmen})

    return df_cr, df_target_cr, df_cyc, df_target_cyc


def get_chart_data_nonpots(filters: dict) -> pd.DataFrame:
    """Fetch aggregated daily/period data for charts."""
    conditions = ["saldo_akhir > 0"]
    where_clause, params = build_where_clause(filters, conditions)
    query = """
        SELECT tanggal, billperiode, SUM(saldo_akhir) as saldo_akhir
        FROM mybrains_nonpots
    """
    query += where_clause + " GROUP BY tanggal, billperiode ORDER BY tanggal ASC"
    return fetch_data(query, params=params)


# ==================== SUPABASE WRITE OPERATIONS ====================

COLUMN_MAPPING_SUPABASE = {
    "idnumber": "idnumber",
    "segmen": "segmen",
    "saldo_akhir": "saldo_akhir",
    "0-3_bln": "0-3_bln",
    "4-6_bln": "4-6_bln",
    "7-12_bln": "7-12_bln",
    "13-24_bln": "13-24_bln",
    ">_24_bln": ">_24_bln",
    "total_billing": "Total Billing",
    "total_collection": "Total Collection",
    "cash": "Cash",
    "non_cash": "Non Cash",
    "bill_bjt": "Bill BJT",
    "coll_bjt": "Coll BJT",
    "cash_bjt": "Cash BJT",
    "tanggal": "tanggal",
    "lama_tunggakan": "lama_tunggakan",
    "kuadran": "kuadran",
    "billperiode": "billperiode",
}


def _convert_currency_to_bigint(df: pd.DataFrame) -> pd.DataFrame:
    """Convert currency columns to bigint format."""
    currency_cols = [
        "saldo_akhir", "0-3_bln", "4-6_bln", "7-12_bln", "13-24_bln", ">_24_bln",
        "total_billing", "total_collection", "cash", "non_cash", "bill_bjt", "coll_bjt", "cash_bjt"
    ]
    for col in currency_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(".", "", regex=False),
                errors="coerce"
            ).fillna(0).astype("int64")
    return df


def _convert_date_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert tanggal from DD/MM/YYYY to YYYY-MM-DD."""
    if "tanggal" in df.columns:
        df["tanggal"] = pd.to_datetime(df["tanggal"], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    return df


def convert_dataframe_to_supabase_format(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert DataFrame to Supabase format with proper column names and data types.
    
    Args:
        df: DataFrame dengan columns dalam snake_case
        
    Returns:
        List of dictionaries ready for Supabase upsert
    """
    df_copy = df.copy()
    df_copy = _convert_currency_to_bigint(df_copy)
    df_copy = _convert_date_format(df_copy)
    
    # Rename dan select columns sesuai mapping
    df_copy = df_copy.rename(columns=COLUMN_MAPPING_SUPABASE)
    columns_to_keep = [COLUMN_MAPPING_SUPABASE[col] for col in df.columns if col in COLUMN_MAPPING_SUPABASE]
    
    return df_copy[columns_to_keep].to_dict(orient="records")


def upsert_mybrains_nonpots_supabase(df: pd.DataFrame, segmen: str, tanggal: str) -> Dict[str, Any]:
    """
    Upsert data ke tabel mybrains_nonpots di Supabase.
    Menghapus data lama untuk segmen dan tanggal yang sama sebelum insert.
    
    Args:
        df: DataFrame dengan data yang akan diupload
        segmen: Segmen pelanggan atau \"-Semua-\"
        tanggal: Tanggal bill periode (format DD/MM/YYYY)
        
    Returns:
        Dict dengan keys: success (bool), upserted (int), error (str/None)
    """
    try:
        records = convert_dataframe_to_supabase_format(df)
        if not records:
            return {"success": False, "error": "Data kosong setelah konversi", "upserted": 0}
        
        supabase = get_supabase_client()
        tanggal_formatted = datetime.strptime(tanggal, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        # Delete old records & upsert new ones
        supabase.table("mybrains_nonpots").delete().eq("segmen", segmen).eq("tanggal", tanggal_formatted).execute()
        supabase.table("mybrains_nonpots").upsert(records).execute()
        
        return {"success": True, "upserted": len(records), "error": None}
        
    except Exception as e:
        return {"success": False, "error": str(e), "upserted": 0}
