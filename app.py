import os
from flask import Flask, render_template, request
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


session = requests.Session()
retry_strategy = Retry(
    total=3,               
    backoff_factor=1,       
    status_forcelist=[429, 500, 502, 503, 504],  
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)


def fetch_movies(query=None, page=1, genre_id=None):
    """Fetch movies by search, genre, or trending"""
    try:
        if query:
            url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}&page={page}"
        elif genre_id:
            url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&page={page}"
        else:
            url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}&page={page}"

        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None


def fetch_genres():
    """Fetch all available genres from TMDB"""
    try:
        url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("genres", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching genres: {e}")
        return []


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    page = int(request.args.get("page", 1))
    genre_id = request.args.get("genre")

    data = fetch_movies(query, page, genre_id)
    genres = fetch_genres()

    movies = []
    total_pages = 1

    if data:
        movies = data.get("results", [])
        total_pages = data.get("total_pages", 1)

    return render_template(
        "index.html",
        movies=movies,
        query=query or "",
        page=page,
        total_pages=total_pages,
        genres=genres,
        selected_genre=genre_id,
        error_message=None if data else "⚠️ Unable to fetch data. Please try again later."
    )


if __name__ == "__main__":
    app.run(debug=True)
