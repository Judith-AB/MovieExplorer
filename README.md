# 🎬 Movie Explorer

Movie Explorer is a simple Flask-based web application that allows you to **search movies** and **filter by genre** using the [TMDB API](https://www.themoviedb.org/documentation/api).  

It provides a clean interface to browse movies with posters, release dates, and short descriptions.  

---

## Features
- 🔎 Search movies by title  
- 🎭 Filter movies by genre  
- ⚠️ Graceful error handling (user-friendly messages when API fails)  
- 📌 "No Movies Found" handling when search/genre returns nothing  
- 🎨 Clean responsive UI with grid layout  

---

## Tech Stack
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS (Jinja2 templating)  
- **API:** TMDB (The Movie Database)  
- **Others:** Requests library  

---

## Getting Started
1️⃣ Clone the repository
git clone https://github.com/YourUsername/MovieExplorer.git
cd MovieExplorer

2️⃣ Create virtual environment
python -m venv venv

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your TMDB API key

Create a .env file in the root directory:

TMDB_API_KEY=your_api_key_here

5️⃣ Run the application
python app.py

## 🎥 Demo Video  

👉 [Watch the demo here](https://drive.google.com/file/d/1uz3cq08nspjfpfvNjKR_5ldj4g1VxZVP/view?usp=sharing) 
