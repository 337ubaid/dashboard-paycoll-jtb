import streamlit as st

from core.schema import SEGMEN_ONLY
from data.supabase import build_where_clause, get_total_saldo
from ui.layout import setup_page
from utils.selector import pilih_all_segmen

setup_page("Supabase", "")

segmen_target = pilih_all_segmen()
tanggal = st.date_input("Pilih Tanggal")

# conn = st.connection("supabase")

# conditions = ["saldo_akhir > 0"]
# params = {}

# if segmen_target in SEGMEN_ONLY:
#     conditions.append("segmen = :segmen")
#     params["segmen"] = segmen_target

# if tanggal:
#     conditions.append("tanggal = :tanggal")
#     params["tanggal"] = tanggal

# query = """
#     SELECT idnumber, segmen, saldo_akhir, tanggal
#     FROM mybrains_nonpots
# """

# query_sum_saldo = """
#     SELECT SUM(saldo_akhir) as total_saldo
#     FROM mybrains_nonpots
# """

# if conditions:
#     where_clause = " WHERE " + " AND ".join(conditions)
#     query += where_clause
#     query_sum_saldo += where_clause

# df = conn.query(
#     query,
#     params=params,
#     ttl=60,
# )
# sum_saldo = conn.query(
#     query_sum_saldo,
#     params=params,
#     ttl=60,
# )


# st.write(tanggal)
# st.write(query_sum_saldo)
# st.write(sum_saldo["total_saldo"].iat[0])
# st.write(query)
# st.write(len(df))
# st.dataframe(df)

###
filters = {
    "segmen": segmen_target,
    "tanggal": tanggal,
}

where_clause, params = build_where_clause(filters)
total_saldo = get_total_saldo(where_clause, params)

st.write(f"filters : {filters}")
st.write(f"where_clause :{where_clause}")
st.write(f"params : {params}")
st.write(total_saldo)
###

conn = st.connection("supabase")
query = """
select * from target_cr
"""

st.write(conn.query(query))