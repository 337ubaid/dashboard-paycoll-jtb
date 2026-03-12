import streamlit as st

def sidebar():
    """
    Fungsi untuk menampilkan menu di sidebar.
    """

    with st.sidebar:
        st.title("Menu")
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link("pages/update_mybrains_nonpots.py", label="Update Daily", icon=":material/event_repeat:")
        st.page_link("pages/kuadran.py", label="Kuadran", icon=":material/dataset:")