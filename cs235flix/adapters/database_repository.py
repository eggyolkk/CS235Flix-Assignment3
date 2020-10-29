import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from cs235flix.domain.model import User, Movie, Review
from cs235flix.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        if target_date is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return movies matching target_date; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie._date == target_date).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(Movie.rank).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie.rank)).first()
        return movie

    def get_first_movie_by_date(self):
        movie = self._session_cm.session.query(Movie).order_by(Movie.release_date).first()
        return movie

    def get_last_movie_by_date(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie.release_date)).first()

    def get_movies_by_rank(self, rank_list):
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]
        movies = []
        for rank in existing_ranks:
            movie = self._session_cm.execute('SELECT rank FROM movies WHERE rank = :rank').fetchall()
            movies.append(movie)

        return movies

    def get_date_of_previous_movie(self, movie: Movie):
        result = None
        prev = self._session_cm.session.query(Movie).filter(Movie.release_date < movie.release_date).order_by(desc(Movie.release_date)).first()

        if prev is not None:
            result = prev.release_date

        return result

    def get_date_of_next_movie(self, movie: Movie):
        result = None
        next = self._session_cm.session.query(Movie).filter(Movie.release_date > movie.release_date).order_by(asc(Movie.reelase_date)).first()

        if next is not None:
            result = next.date

        return result

    def get_movie_ranks_for_type(self, movies: list):
        rank_list = []

        for movie in movies:
            rank = self._session_cm.execute('SELECT rank FROM movies WHERE title = :movie.title').fetchall()
            rank_list.append(rank)

        return rank_list

    def get_movie_by_type(self, search: str, type_var: str):
        movies = []
        search = search.lower()

        if type_var == "actor":
            movie = self._session_cm.query(Movie).filter(search in Movie.actors).all()

        elif type_var == "director":
            movie = self._session_cm.query(Movie).filter(search in Movie.director).all()
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

            for genre in stripped:
                movie = self._session_cm.query(Movie).filter(genre in Movie.genres).all()

        elif type_var == "movie":
            movie = self._session_cm.query(Movie).filter(search == Movie.title).all()


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            movie_data = row
            movie_key = movie_data[0]

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            yield movie_data


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    insert_movies = """
        INSERT INTO movies (
        id, title, release_date, rank, description, director, actors, genres)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_users = """
        INSERT INTO users(
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user()))

    conn.commit()
    conn.close()
