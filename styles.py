# =============================
# Theme & Styling System
# =============================

CINEMA_THEME_CSS = """
<style>
* {
    margin: 0;
    padding: 0;
}

:root {
    --primary-color: #ff3d81;
    --secondary-color: #7f5cff;
    --accent-color: #2fd1ff;
    --dark-bg: #05070f;
    --card-bg: rgba(255, 255, 255, 0.06);
    --card-bg-strong: rgba(17, 24, 39, 0.72);
    --text-primary: #f8fbff;
    --text-secondary: #b3bfd3;
    --border-color: rgba(255, 255, 255, 0.14);
    --glow-primary: rgba(255, 61, 129, 0.35);
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 12% 18%, rgba(255, 61, 129, 0.22), transparent 32%),
        radial-gradient(circle at 84% 14%, rgba(127, 92, 255, 0.24), transparent 34%),
        radial-gradient(circle at 52% 100%, rgba(47, 209, 255, 0.15), transparent 36%),
        linear-gradient(165deg, #04050b 0%, #0b1022 55%, #131a36 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(5, 7, 15, 0.96) 0%, rgba(13, 19, 40, 0.96) 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.stContainer {
    max-width: 1460px;
}

/* Header Styling */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700;
    letter-spacing: -0.5px;
}

h1 {
    font-size: 3.15rem !important;
    background: linear-gradient(120deg, #ffffff 10%, #f4c7ff 42%, #a7c6ff 75%, #7ae7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem !important;
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
    margin-bottom: 1.25rem;
    line-height: 1.6;
}

.cinema-hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--border-color);
    border-radius: 22px;
    padding: 1.8rem 1.6rem 1.6rem 1.6rem;
    margin-bottom: 1.7rem;
    background:
        linear-gradient(120deg, rgba(255, 61, 129, 0.12), transparent 40%),
        linear-gradient(305deg, rgba(47, 209, 255, 0.12), transparent 35%),
        var(--card-bg-strong);
    box-shadow:
        0 16px 45px rgba(0, 0, 0, 0.42),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.cinema-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        90deg,
        rgba(255,255,255,0.02) 0px,
        rgba(255,255,255,0.02) 1px,
        transparent 1px,
        transparent 9px
    );
    pointer-events: none;
}

.hero-pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}

.hero-pill {
    font-size: 0.78rem;
    color: #e9f3ff;
    border: 1px solid rgba(255,255,255,0.22);
    background: rgba(255, 255, 255, 0.06);
    border-radius: 999px;
    padding: 0.32rem 0.72rem;
}

/* Movie Card Styling */
.movie-card {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.04));
    border: 1px solid var(--border-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(4px);
}

.movie-card:hover {
    transform: translateY(-8px) scale(1.018);
    border-color: var(--primary-color);
    box-shadow:
        0 0 0 1px rgba(255, 61, 129, 0.6),
        0 0 24px rgba(255, 61, 129, 0.45),
        0 26px 52px var(--glow-primary);
}

.movie-card:hover img {
    filter: drop-shadow(0 0 16px rgba(255, 61, 129, 0.6)) brightness(1.08);
}

.movie-card-content {
    display: block;
}

.movie-card-link {
    display: block;
    border-radius: 16px;
    transition: inherit;
}

.movie-card-link:hover {
    text-decoration: none;
}

.movie-card [data-testid="stButton"] {
    position: relative;
    z-index: 4;
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
    background: linear-gradient(135deg, #ff3d81, #7f5cff);
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
    background: rgba(255, 255, 255, 0.045) !important;
    border: 1.5px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 14px !important;
    padding: 0.78rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 24px var(--glow-primary) !important;
}

/* Button Styling */
button {
    background: linear-gradient(135deg, #ff3d81, #7f5cff) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 0.58rem 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
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
    background: rgba(255, 61, 129, 0.09) !important;
    border: 1px solid rgba(255, 61, 129, 0.35) !important;
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
    background: rgba(47, 209, 255, 0.08) !important;
    border: 1px solid rgba(47, 209, 255, 0.35) !important;
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

.cinema-section-tag {
    font-size: 0.8rem;
    color: #f3f6ff;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 999px;
    display: inline-block;
    padding: 0.28rem 0.75rem;
    margin-bottom: 0.75rem;
    background: rgba(255, 255, 255, 0.04);
}
</style>
"""


def apply_theme():
    """Apply cinema theme styling to Streamlit app"""
    import streamlit as st
    st.markdown(CINEMA_THEME_CSS, unsafe_allow_html=True)
