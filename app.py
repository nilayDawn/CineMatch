import requests
import streamlit as st
import importlib
try:
    st_searchbox = importlib.import_module("streamlit_searchbox").st_searchbox
except Exception:
    st_searchbox = None

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# MODERN DARK THEME STYLES
# =============================
st.markdown(
    """
<style>
* {
    margin: 0;
    padding: 0;
}

:root {
    --primary-color: #FF006E;
    --secondary-color: #8338EC;
    --accent-color: #3A86FF;
    --dark-bg: #0a0e27;
    --card-bg: #1a1f3a;
    --text-primary: #ffffff;
    --text-secondary: #b8c5d6;
    --border-color: #2d3561;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
}

.stContainer {
    max-width: 1400px;
}

/* Header Styling */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700;
    letter-spacing: -0.5px;
}

h1 {
    font-size: 3rem !important;
    background: linear-gradient(135deg, #FF006E, #3A86FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-size: 2rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1.5rem !important;
}

h3 {
    font-size: 1.5rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* Text Colors */
p, span, label {
    color: var(--text-secondary) !important;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Movie Card Styling */
.movie-card {
    border-radius: 12px;
    overflow: hidden;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}

.movie-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: var(--primary-color);
    box-shadow: 0 20px 40px rgba(255, 0, 110, 0.2);
}

.movie-card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    padding: 0.75rem 0.5rem 0 0.5rem;
    line-height: 1.3;
    min-height: 2.6rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.movie-card-meta {
    font-size: 0.8rem;
    color: var(--text-secondary);
    padding: 0 0.5rem 0.5rem 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.rating-badge {
    background: linear-gradient(135deg, #FF006E, #8338EC);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.75rem;
}

/* Search Bar Styling */
.search-container {
    position: relative;
    margin-bottom: 2rem;
}

[data-testid="stTextInput"] {
    background: var(--card-bg) !important;
}

[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 20px rgba(255, 0, 110, 0.3) !important;
}

/* Button Styling */
button {
    background: linear-gradient(135deg, #FF006E, #8338EC) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(255, 0, 110, 0.3) !important;
}

/* Tabs Styling */
[data-testid="stTabs"] [role="tablist"] button {
    color: var(--text-secondary) !important;
    border-bottom: 3px solid transparent !important;
    background: transparent !important;
    padding: 1rem !important;
}

[data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] {
    color: var(--primary-color) !important;
    border-bottom-color: var(--primary-color) !important;
}

/* Divider */
hr {
    border-color: var(--border-color) !important;
    margin: 2rem 0 !important;
}

/* Info/Warning Messages */
[data-testid="stAlert"] {
    background: rgba(255, 0, 110, 0.1) !important;
    border: 1px solid rgba(255, 0, 110, 0.3) !important;
    border-radius: 12px !important;
    color: var(--text-secondary) !important;
}

/* Sidebar */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--text-primary) !important;
}

[data-testid="stSelectbox"], [data-testid="stSlider"] {
    color: var(--text-secondary) !important;
}

/* Backdrop Image Overlay */
.backdrop-hero {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.backdrop-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(10, 14, 39, 0.95), rgba(10, 14, 39, 0.3), transparent);
    padding: 2rem;
    color: white;
}

/* Recommendation Sections */
.section-header {
    padding: 1.5rem 0;
    border-left: 4px solid var(--primary-color);
    padding-left: 1rem;
}

.section-subtitle {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

/* Loading and Empty States */
[data-testid="stInfo"], [data-testid="stWarning"] {
    background: rgba(58, 134, 255, 0.1) !important;
    border: 1px solid rgba(58, 134, 255, 0.3) !important;
    border-radius: 12px !important;
}

/* Compact autocomplete panel (search area) */
.autocomplete-shell {
    margin-top: 0.35rem;
    margin-bottom: 0.6rem;
    padding: 0.45rem 0.55rem 0.2rem 0.55rem;
    border: 1px solid rgba(58, 134, 255, 0.35);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.autocomplete-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-bottom: 0.35rem;
    padding-left: 0.2rem;
    letter-spacing: 0.02em;
}

/* Main-area select styling (autocomplete look) */
[data-testid="stAppViewContainer"] div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 10px !important;
    min-height: 2.3rem !important;
}

[data-testid="stAppViewContainer"] div[data-baseweb="select"] input {
    color: var(--text-primary) !important;
}

/* Keep sidebar select controls lighter */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: none !important;
}

.quick-suggestions-caption {
    margin-top: 0.25rem;
    margin-bottom: 0.45rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

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
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


from typing import Optional, List, Dict, Any

def movie_card(title: str, poster: Optional[str] = None, rating: Optional[float] = None, year: Optional[str] = None, tmdb_id: Optional[int] = None, key_prefix: str = "card"):
    """Enhanced movie card with rating and hover effects"""
    if poster:
        st.image(poster, width=180)
    else:
        st.markdown(
            "<div style='width:180px;height:270px;background:var(--card-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;'>"
            "<p style='color:var(--text-secondary);'>🖼️ No Poster</p></div>",
            unsafe_allow_html=True
        )
    
    st.markdown(f"<div class='movie-card-title'>{title}</div>", unsafe_allow_html=True)
    
    # Meta info
    meta_html = "<div class='movie-card-meta'>"
    if year:
        meta_html += f"<span>{year}</span>"
    if rating:
        meta_html += f"<span class='rating-badge'>⭐ {rating:.1f}</span>"
    meta_html += "</div>"
    st.markdown(meta_html, unsafe_allow_html=True)
    
    if st.button("View Details", key=f"{key_prefix}_{tmdb_id}", use_container_width=True):
        if tmdb_id:
            goto_details(tmdb_id)


def poster_grid(cards, cols=6, key_prefix="grid"):
    """Display cards in a responsive grid with enhanced styling"""
    if not cards:
        st.info("😴 No movies to show. Try a different search or category!")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="medium")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            rating = m.get("vote_average")
            year = (m.get("release_date") or "")[:4]

            with colset[c]:
                st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                movie_card(title, poster, rating, year, tmdb_id, f"{key_prefix}_{r}_{c}")
                st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


def live_movie_suggestions(search_term: str) -> List[str]:
    """Used by live search component: fetch suggestions while typing."""
    query = (search_term or "").strip()

    if len(query) < 2:
        st.session_state["live_search_query"] = query
        st.session_state["live_search_suggestions"] = []
        st.session_state["live_search_cards"] = []
        st.session_state["live_label_to_id"] = {}
        st.session_state["live_search_error"] = None
        return []

    data, err = api_get_json("/tmdb/search", params={"query": query})
    if err or data is None:
        st.session_state["live_search_query"] = query
        st.session_state["live_search_suggestions"] = []
        st.session_state["live_search_cards"] = []
        st.session_state["live_label_to_id"] = {}
        st.session_state["live_search_error"] = err or "Unknown error"
        return []

    suggestions, cards = parse_tmdb_search_to_cards(data, query, limit=24)
    label_to_id = {label: tmdb_id for label, tmdb_id in suggestions}

    st.session_state["live_search_query"] = query
    st.session_state["live_search_suggestions"] = suggestions
    st.session_state["live_search_cards"] = cards
    st.session_state["live_label_to_id"] = label_to_id
    st.session_state["live_search_error"] = None

    return [label for label, _ in suggestions]


# =============================
# SIDEBAR (Modern Navigation)
# =============================
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    st.markdown("<p class='subtitle'>Your Personal Movie Recommender</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True, key="home_btn"):
        goto_home()
    
    st.markdown("---")
    st.subheader("📽️ Explore by Category")
    home_category = st.selectbox(
        "Select Category:",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.subheader("⚙️ Settings")
    grid_cols = st.slider("Movies per row:", 4, 8, 6, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.8rem; color: var(--text-secondary);'>CineMatch v1.0 • Powered by TMDB</p>", unsafe_allow_html=True)

# =============================
# HEADER (Modern Hero Section)
# =============================
st.markdown("<h1>🎬 CineMatch</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Discover movies tailored to your taste. Search, explore, and find your next favorite film.</p>",
    unsafe_allow_html=True,
)

# ==========================================================
# VIEW: HOME (Modern Search & Discovery)
# ==========================================================
if st.session_state.view == "home":
    # Search Section
    st.markdown("### 🔍 Search for Movies")
    if st_searchbox is not None:
        selected_label = st_searchbox(
            search_function=live_movie_suggestions,
            placeholder="Type movie name...",
            label="Movie search",
            clear_on_submit=False,
            key="movie_live_search",
        )

        # Navigate only when user selects an item from dropdown
        if selected_label:
            if st.session_state.get("last_selected_label") != selected_label:
                st.session_state["last_selected_label"] = selected_label
                tmdb_id = st.session_state.get("live_label_to_id", {}).get(selected_label)
                if tmdb_id:
                    goto_details(int(tmdb_id))

        typed = st.session_state.get("live_search_query", "").strip()
        suggestions = st.session_state.get("live_search_suggestions", [])
        cards = st.session_state.get("live_search_cards", [])
        live_err = st.session_state.get("live_search_error")

        if typed and len(typed) < 2:
            st.caption("✏️ Type at least 2 characters to see suggestions.")
            st.stop()

        if typed and len(typed) >= 2:
            if live_err:
                st.error(f"❌ Search failed: {live_err}")
                st.stop()

            if suggestions:
                st.markdown("<div class='quick-suggestions-caption'>⚡ Quick Suggestions</div>", unsafe_allow_html=True)
                quick_cols = st.columns(5)
                for i, (label, tmdb_id) in enumerate(suggestions[:5]):
                    with quick_cols[i % 5]:
                        if st.button(label, key=f"quick_suggestion_{tmdb_id}", use_container_width=True):
                            goto_details(tmdb_id)

                st.markdown("---")
                st.markdown(f"### 📽️ Results for '{typed}'")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
            else:
                st.caption("😕 No movies found. Try a different search!")
            st.stop()
    else:
        # Fallback when live component is unavailable
        typed = st.text_input(
            "Enter movie title",
            placeholder="e.g., Inception, Dune, Parasite...",
            label_visibility="collapsed",
        )

        if typed.strip() and len(typed.strip()) >= 2:
            with st.spinner("🔎 Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"❌ Search failed: {err}")
                st.stop()

            suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
            if suggestions:
                labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                selected = st.selectbox("Search suggestions", labels, index=0, label_visibility="collapsed")
                if selected != "-- Select a movie --":
                    label_to_id = {s[0]: s[1] for s in suggestions}
                    goto_details(label_to_id[selected])

                st.markdown("<div class='quick-suggestions-caption'>⚡ Quick Suggestions</div>", unsafe_allow_html=True)
                quick_cols = st.columns(5)
                for i, (label, tmdb_id) in enumerate(suggestions[:5]):
                    with quick_cols[i % 5]:
                        if st.button(label, key=f"quick_fallback_{tmdb_id}", use_container_width=True):
                            goto_details(tmdb_id)

                st.markdown("---")
                st.markdown(f"### 📽️ Results for '{typed.strip()}'")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
            else:
                st.caption("😕 No movies found. Try a different search!")
            st.stop()

        if typed.strip() and len(typed.strip()) < 2:
            st.caption("✏️ Type at least 2 characters to see suggestions.")
            st.stop()

    # HOME FEED (Default)
    st.markdown("---")
    st.markdown(f"### 🎯 Trending — {home_category.replace('_', ' ').title()}")
    st.markdown(f"<p class='section-subtitle'>Check out the hottest movies right now</p>", unsafe_allow_html=True)

    with st.spinner("⏳ Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )
    
    if err or not home_cards:
        st.error(f"❌ Failed to load movies: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS (Movie Detail Page with Recommendations)
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("⚠️ No movie selected.")
        if st.button("← Back to Home", use_container_width=True):
            goto_home()
        st.stop()

    # Back button
    if st.button("← Back to Home (Top)", key="back_top"):
        goto_home()

    # Load movie details
    with st.spinner("⏳ Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"❌ Could not load details: {err or 'Unknown error'}")
        if st.button("← Go Home"):
            goto_home()
        st.stop()

    # Hero Section with Backdrop
    title = data.get("title", "Unknown")
    overview = data.get("overview") or "No overview available."
    release_date = data.get("release_date") or "N/A"
    genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "N/A"
    poster_url = data.get("poster_url")
    backdrop_url = data.get("backdrop_url")

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

    # Movie Info Layout
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

    # Recommendations Section with Tabs
    st.markdown("### 🎯 Recommended for You")
    st.markdown(f"<p class='section-subtitle'>Based on title similarity and genre preferences</p>", unsafe_allow_html=True)

    title_str = (data.get("title") or "").strip()
    if title_str:
        with st.spinner("🔄 Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            # Create tabs for different recommendation types
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
    st.markdown("<p style='text-align: center; color: var(--text-secondary); font-size: 0.85rem;'>",
                unsafe_allow_html=True)
    if st.button("← Back to Home (Bottom)", use_container_width=True, key="back_bottom"):
        goto_home()
    st.markdown("</p>", unsafe_allow_html=True)