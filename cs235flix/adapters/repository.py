import abc
from typing import List

from cs235flix.domain.model import Movie, User, Review


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, rank: int) -> Movie:
        """ Returns Movie with rank from the repository.

         If there is no Movie with the given rank, this method returns None.
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        """ Returns a list of Movies that were published on target_date.

        If there are no Movies on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by rank, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by rank, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie_by_date(self) -> Movie:
        """ Returns the first Movie, ordered by date, from the repository.

        Returns None if the repository is empty.
        """

    @abc.abstractmethod
    def get_last_movie_by_date(self) -> Movie:
        """ Returns the last Movie, ordered by date, from the repository.

        Returns None if the repository is empty.
        """

    @abc.abstractmethod
    def get_movies_by_rank(self, rank_list):
        """ Returns a list of Movies, whose ranks match those in rank_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_previous_movie(self, movie: Movie):
        """ Returns the date of a Movie that immediately precedes movie.

        If movie is the first Movie in the repository, this method returns None because there are no Movies
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_next_movie(self, movie: Movie):
        """ Returns the date of a Movie that immediately follows movie.

        If movie is the last Movie in the repository, this method returns None because there are no Movies
        on a later date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_type(self, search: str, type_var: str):
        """ Returns movies with starring actors / by director specified in search.

        If no matches found, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_type(self, movies: list):
        """ Returns a list of ranks for the movie list provided.

        If the movie list is empty, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_search(self, search: str):
        """ Set the current search to user input.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_search(self):
        """ Return the current search.

        If no searches found, return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Movie and a User, this method raises a
        Repository Exception and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_watchlist(self, movie: Movie):
        """ Adds a Movie to repository watchlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_watchlist(self):
        """ Returns the Movies stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def check_if_added(self, movie_rank: int):
        """ Returns True if movie has been added to watchlist.

        If the movie hasn't been added, this method returns False.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def years_list(self):
        """ Returns a list of the release dates of all movies.

        If movies list is empty, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_posters_by_movies(self, movies):
        """ Sets posters to the movies. """
        raise NotImplementedError
