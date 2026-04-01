# =============================
# Search & Parsing Utilities
# =============================

import streamlit as st
from typing import List, Tuple, Dict, Any
from api import api_get_json
from config import TMDB_IMG, MIN_SEARCH_LENGTH
import importlib

# Try to import live search component
try:
    st_searchbox = importlib.import_module("streamlit_searchbox").st_searchbox
except Exception:
    st_searchbox = None


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24) -> Tuple[List[Tuple[str, int]], List[Dict]]:
    """
    Parse TMDB API response to search suggestions and cards.
    
    Supports both API response shapes:
    - Raw TMDB: {"results":[{id,title,poster_path,...}]}
    - Card list: [{tmdb_id,title,poster_url,...}]
    
    Returns:
        (suggestions: List[(label, tmdb_id)], cards: List[{tmdb_id,title,poster_url}])
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

    # If nothing matched, fallback to raw list
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
    """
    Live search suggestions callback.
    Fetches and caches suggestions while user types.
    """
    query = (search_term or "").strip()

    if len(query) < MIN_SEARCH_LENGTH:
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
