# Cyberflix

Cyberflix — a small Netflix-inspired streaming MVP (Flask + SQLite).

This repository contains an initial scaffold and ongoing implementation for the Cyberflix MVP: Flask backend, SQLite models, authentication, pages (login/signup/home/catalogue/movie details), and seeded sample data.

Setup (development)
1. Clone the repo (you must have access to the private repository):
   - git clone git@github.com:cyberjet-hub/cyberflix.git
2. Create and activate a virtualenv:
   - python -m venv venv
   - source venv/bin/activate   (Windows: venv\Scripts\activate)
3. Install dependencies:
   - pip install -r requirements.txt
4. Create an instance .env file and set a strong secret:
   - cp instance/.env.example instance/.env
   - Edit instance/.env and set FLASK_SECRET to a strong secret (do NOT commit this file).
5. Run the app:
   - python run.py
6. Open http://127.0.0.1:5000

Notes
- The app uses SQLite by default and will create a local database file when started.
- Seed data loads a few sample movies on first run. Sample video URL is a permissively licensed demo.
- For production: provide DATABASE_URL and FLASK_SECRET environment variables, use a production WSGI server, and host media on a secure storage service.
