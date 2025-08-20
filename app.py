import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app = Flask(__name__)

# Setup requests session with retries
session = requests.Session()
retries = Retry(
    total=3,               # Retry 3 times
    backoff_factor=0.5,    # Wait 0.5s, then 1s, then 2s between retries
    status_forcelist=[500, 502, 503, 504]  # Retry only on server errors
)
session.mount("https://", HTTPAdapter(max_retries=retries))


def fetch_movies(query=None, page=1, genre_id=None):
    """Fetch movies from TMDb API with search, genre, or popular fallback."""
    try:
        url = "https://api.themoviedb.org/3/search/movie" if query else \
              "https://api.themoviedb.org/3/discover/movie"

        params = {
            "api_key": TMDB_API_KEY,
            "page": page,
            "with_genres": genre_id if genre_id else None
        }
        if query:
            params["query"] = query

        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "⏳ Server took too long to respond. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "⚠️ Network issue. Please check your connection."}
    except Exception:
        return {"error": "❌ Unexpected error fetching movies."}


def fetch_genres():
    """Fetch available movie genres from TMDb API."""
    try:
        url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {"api_key": TMDB_API_KEY}
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("genres", [])
    except Exception:
        return []


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    page = int(request.args.get("page", 1))
    genre_id = request.args.get("genre")

    # Fetch genres for dropdown
    genres = fetch_genres()

    # Fetch movies
    data = fetch_movies(query, page, genre_id)
    error = None
    movies = []
    total_pages = 1

    if "error" in data:
        error = data["error"]
    else:
        movies = data.get("results", [])
        total_pages = data.get("total_pages", 1)

    return render_template(
        "index.html",
        movies=movies,
        error=error,
        page=page,
        total_pages=total_pages,
        query=query or "",
        genres=genres,
        selected_genre=genre_id
    )


if __name__ == "__main__":
    app.run(debug=True)
