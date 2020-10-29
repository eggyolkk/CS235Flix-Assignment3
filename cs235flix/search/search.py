from flask import Blueprint, render_template, redirect, url_for, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import cs235flix.search.services as services
import cs235flix.adapters.repository as repo

# Configure Blueprint.
search_blueprint = Blueprint(
    'search_bp', __name__
)


@search_blueprint.route('/actor', methods=['GET', 'POST'])
def actor():
    form = ActorSearchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the input for actor has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.actor.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_bp.results', search_type="actor"))

    # Request the display page
    return render_template(
        'search/search_page.html',
        title='Search results',
        search_variable="actor",
        handler_url=url_for('search_bp.actor'),
        form=form
    )


@search_blueprint.route('/director', methods=['GET', 'POST'])
def director():
    form = DirectorSearchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the input for director has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.director.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_bp.results', search_type="director"))

    # Request the display page
    return render_template(
        'search/search_page.html',
        title='Search results',
        search_variable="director",
        handler_url=url_for('search_bp.director'),
        form=form
    )


@search_blueprint.route('/genre', methods=['GET', 'POST'])
def genre():
    form = GenreSearchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the input for genre/genres has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.genre.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_bp.results', search_type="genres"))

    # Request the display page
    return render_template(
        'search/search_page.html',
        title='Search results',
        search_variable="genre",
        handler_url=url_for('search_bp.genre'),
        form=form
    )


@search_blueprint.route('/movie', methods=['GET', 'POST'])
def movie():
    form = MovieSearchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the input for movie has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.movie.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_bp.results', search_type="movie"))

    # Request the display page
    return render_template(
        'search/search_page.html',
        title='Search results',
        search_variable="movie",
        handler_url=url_for('search_bp.movie'),
        form=form
    )


@search_blueprint.route('/results', methods=['GET'])
def results():
    movies_per_page = 5

    # Read query parameters
    cursor = request.args.get('cursor')
    search_type = request.args.get('search_type')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    added_movie = request.args.get('added_movie')

    movies, specification, search, count, plural, first_movie_url, last_movie_url, next_movie_url, prev_movie_url, \
        movie_for_poster = results_helper(search_type, movie_to_show_reviews, cursor, movies_per_page)

    if movie_to_show_reviews is not None:
        movie_to_show_reviews = int(movie_to_show_reviews)

    return render_template(
        'movies/browse_movies.html',
        movies=movies,
        name=specification + str(search).capitalize() + "'",
        count=count,
        movie_plural=plural,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        next_movie_url=next_movie_url,
        prev_movie_url=prev_movie_url,
        page="search",
        search_type=search_type,
        search_movie_poster=movie_for_poster,
        search_text=str(search),
        show_reviews_for_movies=movie_to_show_reviews,
        added_movie=added_movie,
        review_type=type(movie_to_show_reviews)
    )


def results_helper(search_type: str, movie_to_show_reviews: int, cursor: int, movies_per_page: int):
    search = services.get_search(repo.repo_instance)
    movies_list = services.search_for_type(search, search_type, repo.repo_instance)
    count = len(movies_list)
    plural = "movies"

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if count == 1:
        plural = "movie"

    if cursor is None:
        # No cursor query parameter so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    # Retrieve movie ranks for movies that have starring actor.
    movie_ranks = services.get_movie_ranks(movies_list, repo.repo_instance)

    # Retrieve the batch of movies to display on web page.
    movies = services.get_movies_by_type(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)
    watch_list = services.get_watchlist(repo.repo_instance)

    services.get_posters(movies, repo.repo_instance)

    for m in movies:
        for added_movie in watch_list:
            if int(m['rank']) == int(added_movie.rank):
                m['watchlist'] = True

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if str(search_type) == "actor":
        specification = "with actor '"
    elif search_type == "director":
        specification = "by director '"
    elif search_type == "movie":
        specification = "by the name '"
    else:
        specification = "with genre(s) '"

    if len(movies) > 0:
        movie_for_poster = str(search)
    else:
        movie_for_poster = "Invalidmovietitle"

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('search_bp.results', search=search, cursor=cursor - movies_per_page,
                                 search_type=search_type)
        first_movie_url = url_for('search_bp.results', search=search)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('search_bp.results', search=search, cursor=cursor + movies_per_page,
                                 search_type=search_type)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('search_bp.results', search=search, cursor=last_cursor, search_type=search_type)

    # Construct urls for viewing movie reviews and adding reviews.
    for m in movies:

        m['view_review_url'] = url_for('search_bp.results', search_cursor=cursor, search_page="search",
                                       view_reviews_for=m['rank'], search_type=search_type)
        m['add_review_url'] = url_for('movies_bp.review_on_movie', movie=m['rank'], search_page="search", search=search,
                                      search_cursor=cursor, search_type=search_type)
        m['add_to_watchlist_url'] = url_for('movies_bp.add_to_watchlist', movie=m['rank'], search_page="search",
                                            search_cursor=cursor, search_type=search_type, search_text=search,
                                            show_reviews_for_movies=movie_to_show_reviews,
                                            name=specification + str(search).capitalize() + "'", movie_plural=plural,
                                            count=count, search_movie_poster=movie_for_poster, page="search",
                                            movies_per_page=movies_per_page)

    return movies, specification, search, count, plural, first_movie_url, last_movie_url, next_movie_url, prev_movie_url, movie_for_poster


class ActorSearchForm(FlaskForm):
    actor = StringField('Search for Movies by Actor', [
        DataRequired(message='Input required'),
        Length(min=3, message='Input too short')
    ])
    submit = SubmitField('Search')


class DirectorSearchForm(FlaskForm):
    director = StringField('Search for Movies by Director', [
        DataRequired(message='Input required'),
        Length(min=3, message='Input too short')
    ])
    submit = SubmitField('Search')


class GenreSearchForm(FlaskForm):
    genre = StringField('Search for Movies by Genre(s) - separate multiple genres with a comma', [
        DataRequired(message='Input required'),
        Length(min=3, message='Input too short')
    ])
    submit = SubmitField('Search')


class MovieSearchForm(FlaskForm):
    movie = StringField('Search for Movies by name', [
        DataRequired(message='Input required')
    ])
    submit = SubmitField('Search')
