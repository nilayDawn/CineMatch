# =============================
# State Management & Routing
# =============================

import streamlit as st


def init_session_state():
    """Initialize session state variables"""
    if "view" not in st.session_state:
        st.session_state.view = "home"  # home | details
    if "selected_tmdb_id" not in st.session_state:
        st.session_state.selected_tmdb_id = None


def sync_query_params_to_state():
    """Sync query parameters to session state"""
    qp_view = st.query_params.get("view")
    qp_id = st.query_params.get("id")
    
    if qp_view in ("home", "details"):
        st.session_state.view = qp_view
    if qp_id:
        try:
            st.session_state.selected_tmdb_id = int(qp_id)
            st.session_state.view = "details"
        except:
            pass


def goto_home():
    """Navigate to home view and clear selection"""
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    """
    Navigate to details view for a movie.
    
    Args:
        tmdb_id: TMDB movie ID
    """
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()
