import pandas as pd


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """
    Load and clean MovieGenre.csv with columns: imdbId, Imdb Link, Title, IMDB Score, Genre, Poster
    Returns DataFrame with columns: imdbId, imdb_link, title, vote_average, genres, poster_url
    """
    # Attempt reading with utf-8, fallback to latin-1
    for enc in ('utf-8', 'latin-1'):
        try:
            df = pd.read_csv(csv_path, encoding=enc, engine='python', on_bad_lines='skip')
            break
        except Exception:
            continue
    # Rename columns
    df = df.rename(columns={
        'imdbId': 'imdbId',
        'Imdb Link': 'imdb_link',
        'Title': 'title',
        'IMDB Score': 'vote_average',
        'Genre': 'genres',
        'Poster': 'poster_url'
    })
    # Drop rows missing essential data
    df = df.dropna(subset=['imdbId', 'imdb_link', 'title', 'vote_average', 'genres', 'poster_url'])
    # Ensure correct types
    df['imdbId'] = df['imdbId'].astype(str)
    df['imdb_link'] = df['imdb_link'].astype(str)
    df['title'] = df['title'].astype(str)
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(0.0)
    df['genres'] = df['genres'].astype(str)
    # Reset index
    return df.reset_index(drop=True)

if __name__ == '__main__':
    print(load_and_clean_data('data/MovieGenre.csv').head())
