# =============================
# View Rendering Functions
# =============================

import streamlit as st
from typing import Optional, Tuple
from api import api_get_json
from components import poster_grid, to_cards_from_tfidf_items
from search import live_movie_suggestions, parse_tmdb_search_to_cards, st_searchbox
from state import goto_home, goto_details
from config import HOME_CATEGORIES, MIN_SEARCH_LENGTH


def render_sidebar() -> Tuple[str, int]:
    """
    Render sidebar with navigation and controls.
    
    Returns:
        (selected_category, grid_columns)
    """
    with st.sidebar:
        st.markdown("## 🎬 CineMatch")
        st.markdown("<p class='subtitle'>Cinema-grade discovery, one click away.</p>", unsafe_allow_html=True)
        st.markdown("---")

        if st.button("🏠 Home", use_container_width=True, key="home_btn"):
            goto_home()

        st.markdown("---")
        st.subheader("📽️ Spotlight")
        home_category = st.selectbox(
            "Select Category:",
            HOME_CATEGORIES,
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.subheader("⚙️ Layout")
        grid_cols = st.slider("Movies per row:", 4, 8, 6, label_visibility="collapsed")

        st.markdown("---")
        st.markdown("<p style='font-size: 0.8rem; color: var(--text-secondary);'>CineMatch v1.0 • </p>", unsafe_allow_html=True)

    return home_category, grid_cols


def render_header():
    """Render main hero/header section"""
    st.markdown(
        """
        <div class='cinema-hero'>
            <h1>🎬 CineMatch</h1>
            <p class='subtitle'>Modern cinematic discovery: search instantly, explore trending titles, and jump into AI-powered recommendations.</p>
            <div class='hero-pill-row'>
                <span class='hero-pill'>Live Search</span>
                <span class='hero-pill'>Poster-first Browsing</span>
                <span class='hero-pill'>TF-IDF Similarity Engine</span>
                <span class='hero-pill'>Genre Companion Picks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_suggestions(suggestions: list, button_prefix: str):
    """
    Display quick suggestion buttons.
    
    Args:
        suggestions: List of (label, tmdb_id) tuples
        button_prefix: Unique prefix for button keys
    """
    st.markdown("<div class='quick-suggestions-caption'>⚡ Quick Suggestions</div>", unsafe_allow_html=True)
    quick_cols = st.columns(5)
    for i, (label, tmdb_id) in enumerate(suggestions[:5]):
        with quick_cols[i % 5]:
            if st.button(label, key=f"{button_prefix}_{tmdb_id}", use_container_width=True):
                goto_details(tmdb_id)


def render_search_results_block(typed: str, cards: list, grid_cols: int):
    """
    Display search results section.
    
    Args:
        typed: Search query text
        cards: List of result cards
        grid_cols: Grid column count
    """
    st.markdown("---")
    st.markdown(f"### 🎞️ Search Results for '{typed}'")
    poster_grid(cards, cols=grid_cols, key_prefix="search_results")


def render_home_feed(home_category: str, grid_cols: int):
    """
    Load and display home feed for selected category.
    
    Args:
        home_category: Category name (trending, popular, etc.)
        grid_cols: Grid column count
    """
    st.markdown("---")
    st.markdown("<span class='cinema-section-tag'>FEATURED</span>", unsafe_allow_html=True)
    st.markdown(f"### 🎯 Now Showing — {home_category.replace('_', ' ').title()}")
    st.markdown("<p class='section-subtitle'>Handpicked from world's hottest feeds right now</p>", unsafe_allow_html=True)

    with st.spinner("⏳ Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )

    if err or not home_cards:
        st.error(f"❌ Failed to load movies: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


def render_home_view(home_category: str, grid_cols: int):
    """
    Main home view with search and featured feed.
    
    Args:
        home_category: Category for featured section
        grid_cols: Grid column count
    """
    st.markdown("<span class='cinema-section-tag'>DISCOVER</span>", unsafe_allow_html=True)
    st.markdown("### 🔍 Find Your Next Watch")

    if st_searchbox is not None:
        selected_label = st_searchbox(
            search_function=live_movie_suggestions,
            placeholder="Type movie name...",
            label="",
            clear_on_submit=False,
            key="movie_live_search",
        )

        if selected_label and st.session_state.get("last_selected_label") != selected_label:
            st.session_state["last_selected_label"] = selected_label
            tmdb_id = st.session_state.get("live_label_to_id", {}).get(selected_label)
            if tmdb_id:
                goto_details(int(tmdb_id))

        typed = st.session_state.get("live_search_query", "").strip()
        suggestions = st.session_state.get("live_search_suggestions", [])
        cards = st.session_state.get("live_search_cards", [])
        live_err = st.session_state.get("live_search_error")

        if typed and len(typed) < MIN_SEARCH_LENGTH:
            st.caption("✏️ Type at least 2 characters to see suggestions.")
            return

        if typed and len(typed) >= MIN_SEARCH_LENGTH:
            if live_err:
                st.error(f"❌ Search failed: {live_err}")
                return

            if suggestions:
                render_quick_suggestions(suggestions, button_prefix="quick_suggestion")
                render_search_results_block(typed, cards, grid_cols)
            else:
                st.caption("😕 No movies found. Try a different search!")
            return

    else:
        typed = st.text_input(
            "Enter movie title",
            placeholder="e.g., Inception, Dune, Parasite...",
            label_visibility="collapsed",
        ).strip()

        if typed and len(typed) < MIN_SEARCH_LENGTH:
            st.caption("✏️ Type at least 2 characters to see suggestions.")
            return

        if typed and len(typed) >= MIN_SEARCH_LENGTH:
            with st.spinner("🔎 Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed})

            if err or data is None:
                st.error(f"❌ Search failed: {err}")
                return

            suggestions, cards = parse_tmdb_search_to_cards(data, typed, limit=24)
            if suggestions:
                labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                selected = st.selectbox("Search suggestions", labels, index=0, label_visibility="collapsed")
                if selected != "-- Select a movie --":
                    label_to_id = {s[0]: s[1] for s in suggestions}
                    goto_details(label_to_id[selected])

                render_quick_suggestions(suggestions, button_prefix="quick_fallback")
                render_search_results_block(typed, cards, grid_cols)
            else:
                st.caption("😕 No movies found. Try a different search!")
            return

    render_home_feed(home_category, grid_cols)


def render_movie_hero(title: str, genres: str, backdrop_url: Optional[str]):
    """
    Render movie hero section with poster/backdrop.
    
    Args:
        title: Movie title
        genres: Comma-separated genre list
        backdrop_url: Backdrop image URL
    """
    if backdrop_url:
        st.markdown(
            f"""
            <div class='backdrop-hero'>
                <img src='{backdrop_url}' style='width:100%;height:400px;object-fit:cover;display:block;'/>
                <div class='backdrop-overlay'>
                    <h2 style='margin-bottom: 0.5rem;'>{title}</h2>
                    <p style='margin-bottom: 1rem; color: #b8c5d6;'>{genres}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)


def render_details_view(grid_cols: int):
    """
    Render detailed movie info with recommendations.
    
    Args:
        grid_cols: Grid column count for recommendations
    """
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("⚠️ No movie selected.")
        if st.button("← Back", use_container_width=True):
            goto_home()
        return

    if st.button("← Back", key="back_top"):
        goto_home()

    with st.spinner("⏳ Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"❌ Could not load details: {err or 'Unknown error'}")
        if st.button("← Back"):
            goto_home()
        return

    title = data.get("title", "Unknown")
    overview = data.get("overview") or "No overview available."
    release_date = data.get("release_date") or "N/A"
    genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "N/A"
    poster_url = data.get("poster_url")
    backdrop_url = data.get("backdrop_url")

    render_movie_hero(title, genres, backdrop_url)

    col1, col2, col3 = st.columns([1, 3, 1], gap="large")

    with col1:
        st.markdown("### 🎬 Poster")
        if poster_url:
            st.image(poster_url, width=200)
        else:
            st.markdown(
                "<div style='width:200px;height:300px;background:var(--card-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;'>"
                "<p style='color:var(--text-secondary);'>🖼️ No Poster</p></div>",
                unsafe_allow_html=True
            )

    with col2:
        st.markdown("### 📋 Details")
        detail_cols = st.columns(2)
        with detail_cols[0]:
            st.metric("📅 Release Date", release_date)
        with detail_cols[1]:
            st.metric("⭐ Rating", f"{data.get('vote_average', 0):.1f}/10" if data.get('vote_average') else "N/A")

        st.markdown("---")
        st.markdown("### 📝 Overview")
        st.write(overview)

    with col3:
        st.markdown("### 🏆 Info")
        st.markdown(f"**Genres**\n\n{genres}")

    st.divider()

    st.markdown("<span class='cinema-section-tag'>RECOMMENDATIONS</span>", unsafe_allow_html=True)
    st.markdown("### 🎯 Recommended for You")
    st.markdown("<p class='section-subtitle'>Based on title similarity and genre preferences</p>", unsafe_allow_html=True)

    title_str = (data.get("title") or "").strip()
    if title_str:
        with st.spinner("🔄 Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tab1, tab2 = st.tabs(["🔊 AI-Powered (TF-IDF)", "🎭 Same Genre"])

            with tab1:
                st.markdown("**Similar movies based on content analysis**")
                tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")

            with tab2:
                st.markdown("**Other popular movies in the same genre**")
                poster_grid(
                    bundle.get("genre_recommendations", []),
                    cols=grid_cols,
                    key_prefix="details_genre",
                )
        else:
            st.info("📊 Showing genre-based recommendations...")
            with st.spinner("⏳ Loading..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )

            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("❌ No recommendations available right now.")
    else:
        st.warning("⚠️ No title available to compute recommendations.")

    st.divider()
    st.markdown("<p style='text-align: center; color: var(--text-secondary); font-size: 0.85rem;'>", unsafe_allow_html=True)
    if st.button("← Back", use_container_width=True, key="back_bottom"):
        goto_home()
    st.markdown("</p>", unsafe_allow_html=True)
