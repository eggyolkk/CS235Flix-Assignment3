from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie, Review
from typing import Iterable


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def set_search(search: str, repo: AbstractRepository):
    # Set the search to a variable in repo.
    repo.set_search(search)


def get_search(repo: AbstractRepository):
    # Retrieve the search user input
    search = repo.get_search()

    return search


def search_for_type(search: str, search_type: str, repo: AbstractRepository):
    # Get list of movies with actor,director, genre(s).
    movies = repo.get_movie_by_type(search, search_type)

    return movies


def get_movie_ranks(movies: list, repo: AbstractRepository):
    rank_list = repo.get_movie_ranks_for_type(movies)

    return rank_list


def get_movies_by_type(rank_list: list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_reviews_for_movie(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


def check_if_added(movie_rank: int, repo: AbstractRepository):
    add = repo.check_if_added(movie_rank)

    return add


def get_watchlist(repo: AbstractRepository):
    watchlist = repo.get_movie_watchlist()

    return watchlist


def get_posters(movies: Iterable[Movie], repo: AbstractRepository):
    repo.get_posters_by_movies(movies)


# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'year': movie.release_date,
        'title': movie.title,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'reviews': reviews_to_dict(movie.reviews),
        'watchlist': False,
        'poster': None
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie_rank': review.movie.rank,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
