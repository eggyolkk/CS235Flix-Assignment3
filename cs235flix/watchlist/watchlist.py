from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask import jsonify

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.utilities.services as util_services
import cs235flix.watchlist.services as services

from cs235flix.authentication.authentication import login_required

# Configure Blueprint.
watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', methods=['GET'])
# @login_required
def watchlist():

    watch_list = services.get_watchlist(repo.repo_instance)

    return render_template(
        'watchlist/watchlist.html',
        title='Watchlist',
        watchlist=watch_list
    )


@watchlist_blueprint.route('/add_to_watchlist', methods=['GET'])
# @login_required
def add_to_watchlist():
    # Obtain the username of the currently logged in user.
    # username = session['username']

    movie_rank = request.args.get('movie')
    search_page = request.args.get('search_page')
    search_cursor = request.args.get('search_cursor')
    search_type = request.args.get('search_type')
    name = request.args.get('name')
    movie_plural = request.args.get('movie_plural')
    count = request.args.get('count')
    search_movie_poster = request.args.get('search_movie_poster')
    search_text = request.args.get('search_text')
    show_reviews_for_movies = request.args.get('show_reviews_for_movies')

    services.add_to_watchlist(int(movie_rank), repo.repo_instance)

    movies_list = services.search_for_type(search_text, search_type, repo.repo_instance)
    movie_ranks = services.get_movie_ranks(movies_list, repo.repo_instance)

    if search_type == "actor" or search_type == "director" or search_type == "genres" or search_type == "movie":
        redirect(url_for('search_bp.results', search=search_text, cursor=search_cursor, view_reviews_for=movie_rank))
    else:
        redirect(url_for('home_bp.home'))

    return render_template(
        'movies/browse_movies.html',
        title='Movies',
        name=name,
        movies=movies_list,
        count=count,
        movie_plural=movie_plural,
        page="search",
        search_type=search_type,
        search_movie_poster=search_movie_poster,
        search_text=search_text,
        show_reviews_for_movies=show_reviews_for_movies
    )