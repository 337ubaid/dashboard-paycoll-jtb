from datetime import datetime

import streamlit as st

from utils.formatter import format_currency, format_headers

PAGES = [
    {
        "page": "app.py",
        "label": "Home",
        "icon": ":material/home:",
    },
    {
        "page": "pages/update_mybrains_nonpots.py",
        "label": "Update Daily",
        "icon": ":material/event_repeat:",
    },
    {
        "page": "pages/kuadran.py",
        "label": "Kuadran",
        "icon": ":material/dataset:",
    },
    {
        "page": "pages/update_batas_kuadran.py",
        "label": "Batas Kuadran",
        "icon": ":material/dataset:",
    },
    {
        "page": "pages/utip.py",
        "label": "UTIP",
        "icon": ":material/money_bag:",
    },
]


def render_sidebar():
    """Render sidebar with navigation menu and sync button."""

    with st.sidebar:
        st.title("Menu")

        # Navigation
        for p in PAGES:
            st.page_link(p["page"], label=p["label"], icon=p["icon"])

        # Sync section
        st.divider()
        _render_sync_section()


def _render_sync_section():
    """Render sync button and last sync time."""
    # Initialize session state
    if "last_sync" not in st.session_state:
        st.session_state.last_sync = None

    # Display last sync time
    if st.session_state.last_sync:
        st.caption(f"🕐 Terakhir sync: {st.session_state.last_sync}")

    # Sync button
    if st.button("🔄 Sync", type="secondary", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.last_sync = datetime.now().strftime("%d/%m/%Y - %H:%M")
        st.success("Data telah disinkronkan!")
        st.rerun()


def print_sort_dataframe(df):
    """Sort dataframe by saldo_akhir (descending) and display."""

    df = df.sort_values("saldo_akhir", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    render_dataframe(df)


def render_dataframe(df):
    """Display dataframe with formatted headers and currency columns."""

    header_map = format_headers(df)
    df = format_currency(df)
    st.dataframe(df, column_config=header_map)
