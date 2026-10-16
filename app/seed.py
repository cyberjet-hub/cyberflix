from flask import url_for
from .models import Movie
from . import db

SAMPLE_VIDEO = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

def seed_sample_data():
    if Movie.query.count() > 0:
        return
    sample = [
        {"title":"A Cosmic Dawn","description":"A short cinematic about sunrise.","genre":"Sci-Fi","release_year":2022,"poster_url":"https://picsum.photos/seed/1/400/600","authorized_video":SAMPLE_VIDEO,"featured":True},
        {"title":"Neon Streets","description":"Nightlife in a neon city.","genre":"Drama","release_year":2021,"poster_url":"https://picsum.photos/seed/2/400/600","authorized_video":SAMPLE_VIDEO},
        {"title":"Ocean Whisper","description":"A calm documentary.","genre":"Documentary","release_year":2020,"poster_url":"https://picsum.photos/seed/3/400/600","authorized_video":SAMPLE_VIDEO}
    ]
    for m in sample:
        movie = Movie(**m)
        db.session.add(movie)
    db.session.commit()
