# Cyberflix

Cyberflix — a small Netflix-inspired streaming MVP (Flask + SQLite).

This repository contains a working MVP scaffold for the Cyberflix app: Flask backend, SQLite models, authentication, homepage, catalogue, movie detail pages, watchlist features, and sample data.

Email verification
- Signup now sends a confirmation token link. To enable real email sending, set SMTP values in `instance/.env`.
- If `MAIL_SERVER` is not configured, the confirmation link is displayed in a flash message for local development.

Setup (development)
1. Clone the repo:
   - `git clone git@github.com:cyberjet-hub/cyberflix.git`

2. Create and activate a virtual environment:
   - `python -m venv venv`
   - `source venv/bin/activate` (Windows: `venv\Scripts\activate`)

3. Install dependencies:
   - `pip install -r requirements.txt`

4. Create a local env file:
   - `cp instance/.env.example instance/.env`
   - Edit `instance/.env` and set a strong `FLASK_SECRET` value. Fill in optional SMTP settings if you want confirmation emails.

5. Run the app:
   - `python run.py`

6. Open:
   - `http://127.0.0.1:5000`

Notes
- The app uses SQLite by default and creates a local database file when started.
- Seed data loads a few sample movies on first run.
- Sample playback uses a public demo video URL; replace with authorized media for production.
- For production, set environment variables and deploy using a production WSGI server such as Gunicorn behind HTTPS.

Features included
- User registration and login
- Secure password hashing with Werkzeug
- Email confirmation flow
- Protected routes using Flask-Login
- Homepage
- Movie catalogue with search and genre filters
- Movie details
- Video player page
- My List page with add/remove watchlist actions
