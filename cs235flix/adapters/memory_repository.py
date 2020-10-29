import csv
import os
from typing import List
import omdb

from bisect import bisect_left, insort_left

from werkzeug.security import generate_password_hash

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Actor, Genre, Director, Movie, User, Review


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


class MemoryRepository(AbstractRepository):
    # Movies ordered by name.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._search = ""
        self._users = list()
        self._reviews = list()
        self._watchlist = list()
        self._years = list()

    @property
    def users(self):
        return self._users

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    @property
    def get_index(self):
        return self._movies_index

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.rank] = movie

    def get_movie(self, rank: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[rank]
        except KeyError:
            # Ignore exception and return None
            pass

        return movie

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        matching_movies = list()

        for m in self._movies:
            if int(m.release_date) == target_date:
                matching_movies.append(m)

        return matching_movies

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_first_movie_by_date(self):
        first_movie = None
        current_year = 3000

        for m in self._movies:
            if int(m.release_date) < current_year:
                current_year = int(m.release_date)
                first_movie = m

        return first_movie

    def get_last_movie_by_date(self):
        last_movie = None
        current_year = 0

        for m in self._movies:
            if int(m.release_date) > current_year:
                current_year = int(m.release_date)
                last_movie = m

        return last_movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies_by_rank(self, rank_list):
        # Strip out any ranks in rank_list that don't represent Movie ranks in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[rank] for rank in existing_ranks]
        return movies

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None
        current_date = 0

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies):
                if int(movie.release_date) > int(stored_movie.release_date) > int(current_date):
                    previous_date = stored_movie.release_date
                    current_date = stored_movie.release_date
        except ValueError:
            # No earlier movies, so return None
            pass

        if previous_date is not None:
            return int(previous_date)
        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None
        current_date = 2020

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies:
                if int(current_date) > int(stored_movie.release_date) > int(movie.release_date):
                    current_date = stored_movie.release_date

                if int(movie.release_date) < int(stored_movie.release_date) <= int(current_date):
                    next_date = stored_movie.release_date
        except ValueError:
            # No subsequent movies, so return None.
            pass

        if next_date is not None:
            return int(next_date)
        return next_date

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_date == movie.release_date:
            return index
        raise ValueError

    def get_movie_ranks_for_type(self, movies: list):
        rank_list = []

        for movie in movies:
            rank_list.append(int(movie.rank))

        return rank_list

    def get_movie_by_type(self, search: str, type_var: str):
        movies = []
        search = search.lower()

        if type_var == "actor":
            for movie in self._movies:
                for actor in movie.actors:
                    if search in str(actor).lower():
                        movies.append(movie)

        elif type_var == "director":
            for movie in self._movies:
                if search in str(movie.director).lower():
                    movies.append(movie)

        elif type_var == "genres":
            genres_list = []
            stripped = []

            if "," in search:
                genres_list = search.split(",")
            else:
                genres_list.append(search.strip())

            for item in genres_list:
                stripped.append(item.strip().lower())

            for movie in self._movies:
                add = True
                for genre in stripped:
                    if genre not in str(movie.genres).lower():
                        add = False

                if add:
                    movies.append(movie)

        elif type_var == "movie":
            for movie in self._movies:
                if search.strip() == str(movie.title).lower():
                    movies.append(movie)

        return movies

    def set_search(self, search: str):
        self._search = search

    def get_search(self):
        return self._search

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def add_to_watchlist(self, movie: Movie):
        if movie not in self._watchlist:
            self._watchlist.append(movie)

    def get_movie_watchlist(self):
        return self._watchlist

    def check_if_added(self, movie_rank: int):
        for movie in self._watchlist:
            if movie.rank == movie_rank:
                return True

        return False

    def years_list(self):
        years_list = []
        for movie in self._movies:
            if int(movie.release_date) not in years_list:
                years_list.append(int(movie.release_date))

        years_list.sort()
        return years_list

    def get_posters_by_movies(self, movies):
        for movie in movies:
            poster = get_poster(movie['title'])
            movie['poster'] = poster


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self._dataset_of_movies = []
        self._dataset_of_actors = []
        self._dataset_of_directors = []
        self._dataset_of_genres = []
        self._dataset_of_descriptions = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                add_rank = row['Rank']
                add_title = row['Title']
                add_year = int(row['Year'])
                add_description = row['Description']
                add_actors = []
                add_genres = []
                add_director = ""

                actors_list = row['Actors'].split(",")
                for a in actors_list:
                    actor = a.strip()
                    add_actor = Actor(actor)
                    if add_actor not in self._dataset_of_actors:
                        self._dataset_of_actors.append(add_actor)
                    add_actors.append(add_actor)

                directors_list = row['Director'].split(",")
                for d in directors_list:
                    add_director = Director(d)
                    if add_director not in self._dataset_of_directors:
                        self._dataset_of_directors.append(add_director)
                    add_director = d

                genre_list = row['Genre'].split(",")
                for g in genre_list:
                    add_genre = Genre(g)
                    if add_genre not in self._dataset_of_genres:
                        self._dataset_of_genres.append(add_genre)
                    add_genres.append(add_genre)

                add_movie = Movie(add_title, add_year, add_rank, add_description, add_director, add_actors, add_genres)
                self._dataset_of_movies.append(add_movie)

                index += 1

    @property
    def dataset_of_movies(self):
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self._dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[0],
            password=generate_password_hash(data_row[1])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_movies(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path, "Data1000Movies.csv"))
    movie_file_reader.read_csv_file()

    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies into the repository
    load_movies(data_path, repo)

    # Load movies into the repository
    load_users(data_path, repo)
