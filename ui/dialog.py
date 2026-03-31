import streamlit as st


@st.dialog("Konfirmasi Upload Data")
def confirm_dialog(on_confirm, on_cancel=None):
    if st.session_state.get("show_confirm", False):
        st.warning("Apakah Anda yakin ingin melanjutkan?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Ya, Upload Sekarang", use_container_width=True):
                on_confirm()
                st.session_state.show_confirm = False
                st.rerun()

        with col2:
            if st.button("❌ Batal", use_container_width=True):
                # if on_cancel:
                #     on_cancel()
                st.session_state.show_confirm = False
                st.rerun()
