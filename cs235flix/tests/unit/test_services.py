import pytest

from cs235flix.movies import services as movies_services
from cs235flix.authentication import services as auth_services
from cs235flix.authentication.services import AuthenticationException


def test_can_add_user(in_memory_repo):
    new_username = 'eb'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    new_username = 'eb'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Add already existing username.
    username = 'eb'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_can_add_review(in_memory_repo):
    # Add user to repository first.
    new_username = 'eb'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Create review
    review_text = "Great movie!"
    movie_rank = 114
    rating = 9

    # Call the service layer to add the review
    movies_services.add_review(movie_rank, review_text, new_username, rating, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_rank, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
    None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    # Add user to repository first.
    new_username = 'eb'
    new_password = 'abcd1A23'
    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Create review
    review_text = "Great movie!"
    movie_rank = 1001
    rating = 9

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_rank, review_text, new_username, rating, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    # Create review
    review_text = "Great movie!"
    movie_rank = 114
    rating = 9
    unknown_user = 'eb'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_rank, review_text, unknown_user, rating, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_rank = 2

    movie_as_dict = movies_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == "Prometheus"
    assert movie_as_dict['year'] == "2012"
    assert movie_as_dict['description'] == "Following clues to the origin of mankind, a team finds a structure on a " \
                                           "distant moon, but they soon realize they are not alone."
    assert str(movie_as_dict['actors']) == "[<Actor Noomi Rapace>, <Actor Logan Marshall-Green>, <Actor Michael " \
                                      "Fassbender>, <Actor Charlize Theron>]"
    assert str(movie_as_dict['genres']) == "[<Genre Adventure>, <Genre Mystery>, <Genre Sci-Fi>]"
    assert str(movie_as_dict['director']) == "<Director Ridley Scott>"


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 1001

    # Call the service layer to attempt to retrieve the Movie
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_rank, in_memory_repo)


def test_get_first_date(in_memory_repo):
    movie_as_dict = movies_services.get_first_date(in_memory_repo)

    # This should return the rank of the first movie of the earliest release date.
    assert movie_as_dict['rank'] == 114


def test_get_last_date(in_memory_repo):
    movie_as_dict = movies_services.get_last_date(in_memory_repo)

    # This should return the rank of the first movie of the latest release date.
    assert movie_as_dict['rank'] == 119


def test_get_movies_by_date_with_multiple_dates(in_memory_repo):
    target_date = 2009

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    assert len(movies_as_dict) == 51
    sample_movie = movies_as_dict[0]
    assert sample_movie.rank == 508

    assert prev_date == 2008
    assert next_date == 2010


def test_get_movies_by_date_with_non_existent_date(in_memory_repo):
    target_date = 2022

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are no movies with the release date of 2022.
    assert len(movies_as_dict) == 0


def test_get_movies_by_rank(in_memory_repo):
    target_movie_ranks = [999, 1000, 1001, 1002]
    movies_as_dict = movies_services.get_movies_by_rank(target_movie_ranks, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the movie ranks returned were 999 and 1000.
    movie_ranks = [movie['rank'] for movie in movies_as_dict]
    assert set([999, 1000]).issubset(movie_ranks)