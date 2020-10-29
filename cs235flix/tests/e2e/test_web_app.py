import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'ella', 'password': 'cLQ^C#oFXloS'}
    )


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('eb', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235Flix' in response.data


@pytest.mark.parametrize(('review', 'messages'),(
        ('Wow', (b'Your review is too short.')),
        ('ass', (b'Your review is too short.'))
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on a movie.
    response = client.post(
        '/review',
        data={'review':review, 'rating': 5, 'movie_rank': 114}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_browse_movies(client):
    # Check that we can retrieve the movies page.
    response = client.get('/browse_by_date')
    assert response.status_code == 200


def test_movies_without_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/browse_by_date')
    assert response.status_code == 200

    # Check that without providing a date query parameter, the page includes the first movie.
    assert b'300' in response.data
    assert b'King Leonidas' in response.data


def test_movies_with_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/browse_by_date?date=2007&cursor=0&max_cursor=53')
    assert response.status_code == 200

    # Check that movies on the requested date are included on the page.
    assert b'1408' in response.data
    assert b'A man who specializes in debunking' in response.data
