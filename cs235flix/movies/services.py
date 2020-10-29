from typing import Iterable, List

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import make_review, Movie, Review

class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_rank: int, review_text: str, username: str, rating, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie, rating)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_date(repo: AbstractRepository):

    movie = repo.get_first_movie_by_date()

    return movie_to_dict(movie)


def get_last_date(repo: AbstractRepository):

    movie = repo.get_last_movie_by_date()

    return movie_to_dict(movie)


def get_movies_by_date(date, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches), the date of the previous movie (might be null), the date
    # of the next movie (might be null)

    movies = repo.get_movies_by_date(int(date))

    prev_date = next_date = None

    if len(movies) > 0:
        prev_date = repo.get_date_of_previous_movie(movies[0])
        next_date = repo.get_date_of_next_movie(movies[0])

    return movies, prev_date, next_date


def get_movies_by_rank(rank_list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


def get_movie_ranks(movies: list, repo: AbstractRepository):
    rank_list = repo.get_movie_ranks_for_type(movies)

    return rank_list


def get_movies_by_type(rank_list: list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def add_to_watchlist(movie_rank: int, repo: AbstractRepository):
    # Check that the movie exists
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    # Update the repository
    repo.add_to_watchlist(movie)

    add = repo.check_if_added(movie_rank)


def get_watchlist(repo: AbstractRepository):
    watchlist = repo.get_movie_watchlist()

    return watchlist


def search_for_type(search: str, search_type: str, repo: AbstractRepository):
    # Get list of movies with actor,director, genre(s).
    movies = repo.get_movie_by_type(search, search_type)

    return movies


def get_dict_watchlist(repo: AbstractRepository):
    watchlist = repo.get_movie_watchlist()

    watchlist_as_dict = movies_to_dict(watchlist)
    return watchlist_as_dict


def get_movies_in_watchlist(rank_list: list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_years(repo: AbstractRepository):
    years_list = repo.years_list()

    return years_list


def get_posters(movies: List[Movie], repo: AbstractRepository):
    repo.get_posters_by_movies(movies)


# ============================================
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
        'timestamp': review.timestamp,
        'rating': review.rating
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def get_years_dict(years_list, url_list, repo: AbstractRepository):
    years_dict = {}
    for i in range(len(years_list)):
        years_dict[years_list[i]] = url_list[i]
    return years_dict