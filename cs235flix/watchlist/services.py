import cs235flix.adapters.repository as repo
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie


class NonExistentMovieException(Exception):
    pass


def add_to_watchlist(movie_rank: int, repo: AbstractRepository):
    # Check that the movie exists
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    # Update the repository
    repo.add_to_watchlist(movie)


def get_watchlist(repo: AbstractRepository):
    watchlist = repo.get_movie_watchlist()

    return watchlist


def search_for_type(search: str, search_type: str, repo: AbstractRepository):
    # Get list of movies with actor/director/genre(s).
    movies = repo.get_movie_by_type(search, search_type)

    return movies


def get_movie_ranks(movies: list, repo: AbstractRepository):
    rank_list = repo.get_movie_ranks_for_type(movies)

    return rank_list

