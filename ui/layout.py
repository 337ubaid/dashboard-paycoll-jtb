import streamlit as st


def render_sidebar():
    """
    Fungsi untuk menampilkan menu di sidebar.
    """

    with st.sidebar:
        st.title("Menu")
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link(
            "pages/update_mybrains_nonpots.py",
            label="Update Daily",
            icon=":material/event_repeat:",
        )
        st.page_link("pages/kuadran.py", label="Kuadran", icon=":material/dataset:")
        st.page_link(
            "pages/update_batas_kuadran.py",
            label="Batas Kuadran",
            icon=":material/dataset:",
        )
        st.page_link(
            "pages/tunggakan_am.py", label="Tunggakan AM", icon=":material/dataset:"
        )
        st.page_link("pages/utip.py", label="UTIP", icon=":material/dataset:")
