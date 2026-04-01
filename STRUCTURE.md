# CineMatch - Movie Recommender

A modern, cinematic movie discovery and recommendation application built with Streamlit and FastAPI.

## 📁 Project Structure

The application is organized into modular, well-structured components for better maintainability:

```
TMDBMOVIE/
├── app.py                 # Main Streamlit entry point
├── config.py             # Configuration constants & settings
├── styles.py             # CSS theme & styling system
├── api.py                # API helpers & request utilities
├── search.py             # Search functionality & parsing
├── components.py         # UI components (cards, grids)
├── state.py              # State management & routing
├── views.py              # View rendering functions
├── main.py               # FastAPI backend (unchanged)
├── movies_metadata.csv   # Movie dataset
├── Movies.ipynb          # Jupyter notebook for analysis
├── requirements.txt      # Python dependencies
└── runtime.txt           # Runtime configuration
```

## 🏗️ Module Descriptions

### `app.py` - Application Entry Point
- Serves as the main Streamlit application entry point
- Initializes page configuration
- Applies theme styling
- Manages routing between home and details views

### `config.py` - Configuration
Contains all configuration constants:
- API endpoints (`API_BASE`, `TMDB_IMG`)
- Page settings
- Home categories list
- Search parameters (minimum length, grid defaults)

### `styles.py` - Theming System
Comprehensive CSS styling with:
- Cinema-grade color palette (neon pink, purple, cyan)
- Glassmorphism effects
- Responsive layouts
- Hover animations and glow effects
- Dark theme with gradient backgrounds

**Functions:**
- `apply_theme()` - Applies CSS to the Streamlit app

### `api.py` - API Communication
Handles all HTTP requests to the FastAPI backend:
- `api_get_json(path, params)` - Safe GET requests with error handling
- 30-second caching for autocomplete suggestions

### `search.py` - Search & Parsing
Movie search functionality:
- `parse_tmdb_search_to_cards()` - Parses API responses into card format
- `live_movie_suggestions()` - Live search autocomplete callback
- Supports both raw TMDB responses and pre-formatted card lists

### `components.py` - UI Components
Reusable UI building blocks:
- `movie_card()` - Enhanced movie card with poster, title, rating, clickability
- `poster_grid()` - Responsive grid layout for movie cards
- `to_cards_from_tfidf_items()` - Converts TF-IDF recommendations to card format

### `state.py` - State Management & Routing
Manages application state and navigation:
- `init_session_state()` - Initializes session variables
- `sync_query_params_to_state()` - Syncs URL query params to session state
- `goto_home()` - Navigate to home view
- `goto_details(tmdb_id)` - Navigate to movie details

### `views.py` - View Rendering
Modular view functions for different UI sections:
- `render_sidebar()` - Navigation and layout controls
- `render_header()` - Hero section with feature pills
- `render_home_view()` - Home page with search and featured feed
- `render_details_view()` - Movie detail page with recommendations
- Helper functions for quick suggestions, search results, etc.

### `main.py` - FastAPI Backend
Unchanged from original. Handles:
- TMDB API integration
- TF-IDF similarity recommendations
- Genre-based recommendations
- Movie metadata endpoints

## 🚀 Getting Started

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI backend
python -m uvicorn main:app --reload

# Run Streamlit app (in another terminal)
streamlit run app.py
```

### URL
- Streamlit app: `http://localhost:8501`
- FastAPI backend: `http://localhost:8000`

## 🎯 Key Features

- **Live Search**: Real-time autocomplete as you type
- **Cinematic UI**: Modern dark theme with neon accents and glassmorphism
- **Hover Effects**: Cards glow and lift on hover
- **Full-Card Clickability**: Click anywhere on the card to view details
- **AI Recommendations**: TF-IDF similarity engine for content-based suggestions
- **Genre Matching**: Shows related movies from the same genre
- **Responsive Grid**: Adjustable columns (4-8) via sidebar slider
- **Category Browse**: Featured feeds (trending, popular, top-rated, etc.)

## 🔄 Data Flow

1. **Home View** → User searches or selects category
2. **Search Results** → Cards displayed with pagination via grid
3. **Movie Details** → Full info with backdrop, poster, metadata
4. **Recommendations** → Two tabs: AI-powered (TF-IDF) + Genre-based
5. **Navigation** → Query params keep URLs shareable

## 🎨 Styling System

All CSS is centralized in `styles.py` with:
- CSS custom properties for colors and spacing
- Responsive grid system
- Smooth transitions and animations
- Glassmorphism with backdrop blur
- Gradient overlays and effects

## 📊 State Management

Uses Streamlit's `st.session_state` + query parameters:
- `view`: Current page ("home" or "details")
- `selected_tmdb_id`: Currently viewing movie ID
- URL sync: `?view=details&id=12345` for shareable links

## ✨ Recent Refactoring

Refactored from a 1700+ line monolithic `app.py` into modular components:
- Separated concerns (config, styling, API, UI, views)
- Improved code maintainability
- Easier to test and extend
- Better code organization

## 📝 Notes

- All imports use relative paths (no package needed)
- CSS-in-JS approach for styling
- Streamlit native components mixed with custom HTML
- Caching strategy for API calls (30s TTL)
