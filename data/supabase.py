import streamlit as st

from core.schema import SEGMEN_ONLY

conn = st.connection("supabase")


def fetch_data(query, where_clause, params, ttl=60):
    query += where_clause
    return conn.query(query, params=params, ttl=ttl)


# queries/builder.py
def build_where_clause(filters: dict):
    conditions = ["saldo_akhir > 0"]
    params = {}

    for key, value in filters.items():
        if value is not None:
            conditions.append(f"{key} = :{key}")
            params[key] = value

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    return where_clause, params


def get_total_saldo(where_clause, params):
    query = f"""
        SELECT SUM(saldo_akhir) as total_saldo
        FROM mybrains_nonpots
    """
    total_saldo = fetch_data(query, where_clause, params)
    return total_saldo["total_saldo"].iat[0]
