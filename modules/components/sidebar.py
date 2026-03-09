import streamlit as st

def sidebar():
    """
    Fungsi untuk menampilkan menu di sidebar.
    """

    with st.sidebar:
        st.title("Menu")
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link("pages/update_daily.py", label="Update Daily", icon=":material/event_repeat:")