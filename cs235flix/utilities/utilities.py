from flask import Blueprint, url_for

import cs235flix.adapters.repository as repo
import cs235flix.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.browse_movies', date=movie['year'])
    return movies
