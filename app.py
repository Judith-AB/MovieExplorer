from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("query", "")
    movies = []
    error_message = None

    if query:
        url = f"https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": query}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            movies = data.get("results", [])

            if not movies:
                error_message = "😕 No movies found. Try another title."
        except requests.exceptions.RequestException:
            error_message = "⚠️ Unable to fetch data right now. Please try again later."

    return render_template("index.html", movies=movies, query=query, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
