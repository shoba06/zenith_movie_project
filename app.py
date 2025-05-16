# app.py
import streamlit as st
import pandas as pd
from preprocess import load_and_clean_data

# --- Page Config ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- Load Data ---
try:
    data = load_and_clean_data("data/MovieGenre.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Header ---
st.title("🎬 Movie Recommendation App")
st.write("Explore movies with posters, filter by genres, and view IMDB ratings.")

# --- Genre Filter ---
st.sidebar.header("🔍 Filter by Genre")
all_genres = sorted({g.strip() for genres in data['genres'] for g in genres.split(',') if g.strip()})
selected_genres = st.sidebar.multiselect("Select Genre(s)", all_genres)

# --- Apply Genre Filter ---
df_filtered = data.copy()
if selected_genres:
    df_filtered = df_filtered[df_filtered['genres'].apply(
        lambda x: any(g.lower() in x.lower() for g in selected_genres)
    )]

# --- Limit Results to 25 ---
df_filtered = df_filtered.head(25)

# --- Display Count ---
st.markdown(f"**Showing {len(df_filtered)} movies** (limited to 25 for speed)")

# --- Movie Grid ---
cols = st.columns(3)
for idx, row in df_filtered.iterrows():
    col = cols[idx % 3]
    with col:
        # Poster with fallback
        try:
            st.image(row['poster_url'], use_column_width=True)
        except Exception:
            st.image("https://via.placeholder.com/300x450?text=No+Image", use_column_width=True)
        # Title with clickable link
        st.markdown(f"### [{row['title']}]({row['imdb_link']})")
        # IMDB Rating
        st.write(f"⭐ IMDB Rating: {row['vote_average']}")
        # Genres
        st.write(f"🎭 Genres: {row['genres']}")