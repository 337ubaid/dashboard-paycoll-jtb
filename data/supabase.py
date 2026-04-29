import streamlit as st

from core.schema import SEGMEN_ONLY

conn = st.connection("supabase")


@st.cache_data(ttl=60)
def fetch_data(query, where_clause=None, params=None):
    final_query = query + (where_clause or "")
    return conn.query(final_query, params=params or {})


# queries/builder.py
def build_where_clause(filters: dict, base_conditions=None):
    conditions = list(base_conditions or [])
    params = {}

    for key, value in filters.items():
        if value is not None:
            conditions.append(f"{key} = :{key}")
            params[key] = value

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    return where_clause, params


def get_metric_tanggal():
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


def get_metric_saldo(filters: dict):
    list_tanggal = get_metric_tanggal()

    filters = filters.copy()
    filters.pop("tanggal", None)

    conditions = ["saldo_akhir > 0"]
    where_clause, params = build_where_clause(filters, conditions)

    # dynamic IN
    placeholders = []
    for i, tgl in enumerate(list_tanggal):
        key = f"tgl_{i}"
        placeholders.append(f":{key}")
        params[key] = tgl

    tanggal_clause = f"tanggal IN ({','.join(placeholders)})"

    where_clause += (
        f" AND {tanggal_clause}" if where_clause else f" WHERE {tanggal_clause}"
    )

    query = """
        SELECT 
            tanggal,
            SUM(saldo_akhir) as total_saldo,
            COUNT(DISTINCT idnumber) as total_pelanggan
        FROM mybrains_nonpots
    """

    query = query + where_clause + " GROUP BY tanggal ORDER BY tanggal DESC"

    df = fetch_data(query, params=params)

    return df


def get_data_nonpots(filters: dict):
    conditions = [
        "saldo_akhir > 0",
        "tanggal = (SELECT MAX(tanggal) FROM mybrains_nonpots)",
    ]
    where_clause, params = build_where_clause(
        filters,
        conditions,
    )
    query = """
        SELECT *
        FROM mybrains_nonpots
    """
    return fetch_data(query, where_clause, params)
