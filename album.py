from typing import List
import ast

class Album:
    def __init__(
        self,
        rank: int,
        title: str,
        artists: List[str],
        average_score: float,
        num_ratings: int,
        num_reviews: int,
        release_date: str,
        primary_genres: List[str],
        secondary_genres: List[str],
        descriptors: List[str],
        rym_href: str,
    ):
        self.rank = rank
        self.title = title
        self.artists = artists
        self.average_score = average_score
        self.num_ratings = num_ratings
        self.num_reviews = num_reviews
        self.release_date = release_date
        self.primary_genres = primary_genres
        self.secondary_genres = secondary_genres
        self.descriptors = descriptors
        self.rym_href = rym_href

    def to_dict(self):
        return {
            "rank": self.rank,
            "title": self.title,
            "artists": self.artists,
            "average_score": self.average_score,
            "num_ratings": self.num_ratings,
            "num_reviews": self.num_reviews,
            "release_date": self.release_date,
            "primary_genres": self.primary_genres,
            "secondary_genres": self.secondary_genres,
            "descriptors": self.descriptors,
            "rym_href": self.rym_href,
        }

    @staticmethod
    def from_dict(data):
        return Album(
            rank=data["rank"],
            title=data["title"],
            artists=data["artists"],
            average_score=data["average_score"],
            num_ratings=data["num_ratings"],
            num_reviews=data["num_reviews"],
            release_date=data["release_date"],
            primary_genres=ast.literal_eval(data["primary_genres"]),
            secondary_genres=data["secondary_genres"],
            descriptors=data["descriptors"],
            rym_href=data["rym_href"],
        )

    def __repr__(self):
        return f"[{self.rank}, {self.title}, {self.artists}, {self.num_ratings}, {self.average_score}, {self.num_reviews}, {self.release_date}, {self.primary_genres}, {self.secondary_genres}, {self.descriptors}, {self.rym_href}]\n"

    def __str__(self):
        return self.__repr__()
