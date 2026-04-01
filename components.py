# =============================
# UI Components
# =============================

import streamlit as st
import html
from typing import Optional, List, Dict
from state import goto_details


def movie_card(title: str, poster: Optional[str] = None, rating: Optional[float] = None, year: Optional[str] = None, tmdb_id: Optional[int] = None, key_prefix: str = "card"):
    """
    Render an enhanced movie card with poster, title, metadata, and hover effects.
    
    Args:
        title: Movie title
        poster: Poster image URL
        rating: Vote average score
        year: Release year
        tmdb_id: TMDB movie ID (for navigation)
        key_prefix: Unique prefix for button keys
    """
    safe_title = html.escape(title, quote=True) if tmdb_id else title
    
    # Build poster HTML
    if poster:
        poster_html = f"<img src='{poster}' alt='{safe_title}' style='width:100%;height:auto;border-radius:12px;display:block;' />"
    else:
        poster_html = "<div style='width:180px;height:270px;background:var(--card-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;'><p style='color:var(--text-secondary);'>🖼️ No Poster</p></div>"
    
    # Build meta HTML
    meta_html = "<div class='movie-card-meta'>"
    if year:
        meta_html += f"<span>{year}</span>"
    if rating:
        meta_html += f"<span class='rating-badge'>⭐ {rating:.1f}</span>"
    meta_html += "</div>"
    
    # Build complete card HTML
    content = f"<div class='movie-card-content'>{poster_html}<div class='movie-card-title'>{safe_title}</div>{meta_html}</div>"
    
    if tmdb_id:
        card_html = f"<a href='?view=details&id={tmdb_id}' class='movie-card-link' style='text-decoration: none; display: block;'>{content}</a>"
    else:
        card_html = content
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    if st.button("Details ▸", key=f"{key_prefix}_{tmdb_id}", use_container_width=True):
        if tmdb_id:
            goto_details(tmdb_id)


def poster_grid(cards: List[Dict], cols: int = 6, key_prefix: str = "grid"):
    """
    Display movie cards in a responsive grid layout.
    
    Args:
        cards: List of movie card dictionaries
        cols: Number of columns
        key_prefix: Unique prefix for button keys
    """
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
                # Use container to properly wrap card styles
                with st.container(border=False):
                    st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                    movie_card(title, poster, rating, year, tmdb_id, f"{key_prefix}_{r}_{c}")
                    st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items: List[Dict]) -> List[Dict]:
    """
    Convert TF-IDF recommendation items to card format.
    
    Args:
        tfidf_items: List of items from TF-IDF recommendations
        
    Returns:
        List of formatted card dictionaries
    """
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
