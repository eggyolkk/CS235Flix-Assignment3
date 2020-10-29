from datetime import datetime

from cs235flix.domain.model import Movie, User, make_review

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "Moana",
        2016,
        "14",
        "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set things right.",
        "Ron Clements",
        "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison",
        "Animation,Adventure,Comedy"
    )


@pytest.fixture()
def user():
    user = User('Ella', '1234567890')
    return User('Ella', '1234567890')


def test_user_construction(user):
    assert user.username == 'Ella'
    assert user.password == '1234567890'
    assert repr(user) == '<User Ella 1234567890>'

    for review in user.reviews:
        # User should have an empty list of Reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.title == "Moana"
    assert movie.rank == 14
    assert movie.release_date == "2016"
    assert movie.description == "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set things right."
    assert movie.actors == "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison"
    assert str(movie.director) == "<Director Ron Clements>"
    assert movie.genres == "Animation,Adventure,Comedy"


def test_movie_less_than_operator(movie):
    movie_1 = movie
    movie_2 = Movie(
        "Inglourious Basterds",
        2009,
        "78",
        "Quentin Tarantino",
        "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same.",
        "Brad Pitt, Diane Kruger, Eli Roth,Mélanie Laurent",
        "Adventure,Drama,War"
    )

    assert movie_2 < movie_1


def test_make_review_establishes_relationships(movie, user):
    review_text = "Great movie!"
    rating = 9
    review = make_review(review_text, user, movie, rating, datetime.today())

    # Check that the User object knows about the Review.
    assert review in user.reviews

    # Check that the Review knows about the User.
    assert review.user is user

    # Check that Article knows about the Comment.
    assert review in movie.reviews

    # Check that the Comment knows about the Article.
    assert review.movie is movie
