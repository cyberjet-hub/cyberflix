from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash, abort
from .models import Movie, Watchlist
from . import db
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured = Movie.query.filter_by(featured=True).limit(1).all()
    trending = Movie.query.limit(6).all()
    return render_template('index.html', featured=featured, trending=trending)

@main_bp.route('/catalogue')
def catalogue():
    q = request.args.get('q', '')
    genre = request.args.get('genre')
    movies = Movie.query
    if q:
        movies = movies.filter(Movie.title.ilike(f"%{q}%"))
    if genre:
        movies = movies.filter_by(genre=genre)
    movies = movies.all()
    return render_template('catalogue.html', movies=movies, q=q, genre=genre)

@main_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)

@main_bp.route('/play/<int:movie_id>')
@login_required
def play(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if not movie.authorized_video:
        flash('This content is not available for playback.', 'warning')
        return redirect(url_for('main.movie_detail', movie_id=movie.id))
    # Simple authorization: only allow playback if movie.authorized_video present
    return render_template('player.html', movie=movie)

@main_bp.route('/my-list')
@login_required
def my_list():
    items = Watchlist.query.filter_by(user_id=current_user.id).all()
    return render_template('mylist.html', items=items)

@main_bp.route('/my-list/add/<int:movie_id>', methods=['POST'])
@login_required
def add_to_list(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    exists = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if exists:
        flash('Already in your list.', 'info')
    else:
        wl = Watchlist(user_id=current_user.id, movie_id=movie.id)
        db.session.add(wl)
        db.session.commit()
        flash('Added to My List.', 'success')
    return redirect(url_for('main.movie_detail', movie_id=movie.id))

@main_bp.route('/my-list/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_list(item_id):
    item = Watchlist.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Removed from My List.', 'success')
    return redirect(url_for('main.my_list'))
