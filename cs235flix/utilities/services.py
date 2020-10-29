from typing import Iterable
import random
import omdb

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ranks = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_ranks)

    return movies_to_dict(movies)


def get_poster(movie: str):
    # Set OMDB API key
    omdb.set_default("apikey", "1454b6c1")
    movies_list = omdb.search_movie(movie)

    # Get poster
    if len(movies_list) != 0:
        poster = movies_list[0]["poster"]
        return poster
    else:
        return None


# ============================================
# Functions to convert dicts to model entities
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'year': movie.release_date,
        'description': movie.description
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
