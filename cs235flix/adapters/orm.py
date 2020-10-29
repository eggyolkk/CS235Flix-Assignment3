from sqlalchemy import (
    Table, MetaData, Column, Integer, String, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from cs235flix.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_date', Integer, nullable=False),
    Column('rank', Integer, nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director', String(255), nullable=False),
    Column('actors', String(1024), nullable=False),
    Column('genres', String(255), nullable=False)
)

search = Table(
    'search', metadata,
    Column('search', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        'username': users.c.username,
        'password': users.column.password,
        'reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_Review__review': reviews.column.review,
        '_Review__timestamp': reviews.column.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_Movie__id': movies.column.id,
        '_Movie__title': movies.column.title,
        '_Movie__release_date': movies.column.release_date,
        '_Movie__rank': movies.column.rank,
        '_Movie__description': movies.column.description,
        '_Movie__director': movies.column.director,
        '_Movie__actors': movies.column.actors,
        '_Movie_genres': movies.column.genres,
        '_Movie_reviews': relationship(model.Review, backref='_movie')
    })

