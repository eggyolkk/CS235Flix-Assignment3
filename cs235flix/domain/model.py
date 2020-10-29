from datetime import datetime
from typing import List, Iterable


class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name: str = actor_full_name.strip()
        self._actor_colleagues: list = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self) -> str:
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return other.__actor_full_name == self.__actor_full_name

    def __lt__(self, other) -> bool:
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self) -> int:
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        self._actor_colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague) -> bool:
        return colleague in self._actor_colleagues


class Genre:
    def __init__(
            self, genre_name: str
    ):
        if genre_name == "":
            self._genre_name: str = "None"
        else:
            self._genre_name: str = genre_name

    @property
    def genre_name(self) -> str:
        return self._genre_name

    def __repr__(self) -> str:
        return f'<Genre {self._genre_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return other._genre_name == self._genre_name

    def __lt__(self, other) -> bool:
        return self._genre_name < other._genre_name

    def __hash__(self) -> int:
        return hash(self._genre_name)


class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name: str = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self) -> str:
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return other.director_full_name == self.__director_full_name

    def __lt__(self, other) -> bool:
        return self.__director_full_name < other.director_full_name

    def __hash__(self) -> int:
        return hash(self.__director_full_name)


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._reviews: List[Review] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username


class Review:
    def __init__(self, user: User, movie: 'Movie', review_text: str, rating: int, timestamp: datetime):
        self.__movie: Movie = movie

        if 1 <= rating <= 10:
            self.__rating: int = int(rating)
        else:
            self.__rating = "N/A"

        self.__user: User = user
        self.__review_text: str = review_text
        self.__timestamp: datetime = datetime.today()

    @property
    def user(self) -> User:
        return self.__user

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __repr__(self) -> str:
        reprstring = str(self.__movie) + ", " + str(self.__timestamp)
        return reprstring

    def __eq__(self, other) -> bool:
        if self.__review_text == other.review_text and self.__movie == other.movie and self.__rating == other.rating and self.__timestamp == other.timestamp:
            return True
        else:
            return False


class Movie:
    def __init__(self, movie_title: str, release_date: int, rank: str, description: str, director: str, actors: [],
                 genres: []):
        if movie_title == "" or type(movie_title) is not str:
            self.__movie_title = None
        else:
            self.__movie_title: str = movie_title.strip()

        self.__id: None
        self.__rank: int = int(rank)
        self.__release_date: int = release_date
        self.__description: str = description
        self.__director: Director = Director(director)
        self.__actors: list = actors
        self.__genres: list = genres
        self.__runtime_minutes: int = 0
        self.__reviews: List[Review] = list()
        self.__poster: str = ""

    @property
    def rank(self) -> int:
        return int(self.__rank)

    @property
    def title(self) -> str:
        return self.__movie_title

    @property
    def release_date(self) -> str:
        return str(self.__release_date)

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> list:
        return self.__actors

    @property
    def genres(self) -> list:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    @property
    def number_of_reviews(self) -> int:
        return len(self.__reviews)

    @property
    def poster(self) -> str:
        return self.__poster

    @title.setter
    def title(self, title):
        self.__title = title

    @release_date.setter
    def release_date(self, release_date):
        if release_date >= 1900:
            self.__release_date = release_date

    @description.setter
    def description(self, description):
        self.__description = description.strip()

    @director.setter
    def director(self, director):
        self.__director = director

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if runtime_minutes > 0:
            self.__runtime_minutes = runtime_minutes
        else:
            raise ValueError

    def __repr__(self) -> str:
        reprstring = "<Movie " + self.__movie_title + ", " + str(self.__release_date) + ">"
        return reprstring

    def __eq__(self, other) -> bool:
        if self.title == other.title and self.__release_date == other.release_date:
            return True
        else:
            return False

    def __lt__(self, other) -> bool:
        if other.title is None:
            return False
        elif self.title < other.title:
            return True
        elif self.title == other.title and self.__release_date < int(other.release_date):
            return True
        else:
            return False

    def __hash__(self) -> int:
        unique_movie = str(self.__movie_title) + str(self.__release_date)
        return hash(unique_movie)

    def add_actor(self, actor):
        if actor not in self.__actors:
            self.__actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        if genre not in self.__genres:
            self.__genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review: Review):
        self.__reviews.append(review)

    def add_poster(self, poster: str):
        self.__poster = poster


class WatchList:
    def __init__(self, user: User):
        self.__user: User = user
        self.__watchlist: list = []
        self.__size: int = len(self.__watchlist)

    @property
    def user(self):
        return self.__user

    @property
    def watchlist(self):
        return self.__watchlist

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            add = True
            for m in self.__watchlist:
                if str(m) == str(movie):
                    add = False
                    break

            if add:
                self.__watchlist.append(movie)
                self.__size += 1

    def remove_movie(self, movie: Movie):
        remove_m = None
        if isinstance(movie, Movie):
            for m in self.__watchlist:
                if m.title == movie.title and m.release_date == movie.release_date:
                    remove_m = m

            if remove_m is not None:
                self.__watchlist.remove(remove_m)
                self.__size -= 1

    def select_movie_to_watch(self, index: int):
        if 0 <= index <= len(self.__watchlist) - 1:
            return self.__watchlist[index]
        else:
            return None

    def size(self):
        return self.__size

    def first_movie_in_watchlist(self):
        if self.__size == 0:
            return None
        else:
            return self.__watchlist[0]

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= self.__size:
            raise StopIteration
        else:
            movie = self.__watchlist[self.i]
            self.i += 1
            return movie


def make_review(review_text: str, user: User, movie: Movie, rating: int, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, rating, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review
