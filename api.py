# =============================
# API Helpers & Utilities
# =============================

import requests
import streamlit as st
from config import API_BASE


@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    """
    Safe TMDB API GET request.
    
    Args:
        path: API endpoint path
        params: Query parameters
        
    Returns:
        Tuple of (data, error_message)
    """
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"
