# =============================
# CineMatch - Main Streamlit App
# =============================
# This is the entry point for the Streamlit application.
# The app is organized into modular components for better maintainability.
#
# Module structure:
# - config.py       : Configuration constants and settings
# - styles.py       : CSS theme and styling system
# - api.py          : API helpers and request utilities
# - search.py       : Search functionality and parsing
# - components.py   : UI components (cards, grids)
# - state.py        : State management and routing
# - views.py        : View rendering functions

import streamlit as st
from styles import apply_theme
from state import init_session_state, sync_query_params_to_state
from views import render_sidebar, render_header, render_home_view, render_details_view


# Configure Streamlit page
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply cinema theme styling
apply_theme()

# Initialize and sync application state
init_session_state()
sync_query_params_to_state()

# Render UI components
home_category, grid_cols = render_sidebar()
render_header()

# Route to appropriate view based on state
if st.session_state.view == "home":
    render_home_view(home_category, grid_cols)
elif st.session_state.view == "details":
    render_details_view(grid_cols)
else:
    st.warning("⚠️ Unknown view. Returning to home.")
    from state import goto_home
    goto_home()
