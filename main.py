from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from decimal import Decimal
import pandas as pd
import os


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
            primary_genres=data["primary_genres"],
            secondary_genres=data["secondary_genres"],
            descriptors=data["descriptors"],
            rym_href=data["rym_href"],
        )

    def __repr__(self):
        return f"[{self.rank}, {self.title}, {self.artists}, {self.num_ratings}, {self.average_score}, {self.num_reviews}, {self.release_date}, {self.primary_genres}, {self.secondary_genres}, {self.descriptors}, {self.rym_href}]\n"

    def __str__(self):
        return self.__repr__()

def save_albums_data_to_csv(*albums, file_path="albums.csv"):
    df = pd.DataFrame([album.to_dict() for album in albums])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

def get_rym_top_albums_data(page=1, driver=webdriver.Chrome()):
    #    driver.get(f"https://rateyourmusic.com/charts/top/album/all-time/{page}/")
    #
    file_path = os.path.abspath("./mock.html")
    driver.get(f"file://{file_path}")
    driver.implicitly_wait(1)
    elements = driver.find_elements(By.CLASS_NAME, "page_section_charts_item_wrapper")
    return elements


def get_album_rank(element: WebElement):
    element_id = element.get_attribute("id")
    return int(element_id[3:])


def get_album_name(element: WebElement):
    album_name_parent_element: WebElement = element.find_element(
        By.CLASS_NAME, "page_charts_section_charts_item_title"
    )
    return album_name_parent_element.text


def get_album_artists(element: WebElement):
    album_artists_parent_element = element.find_elements(By.CLASS_NAME, "artist")
    album_artists_names = [
        element.text[:-1].strip() if element.text.endswith("&") else element.text
        for element in album_artists_parent_element
    ]
    return album_artists_names


def get_album_num_ratings(element: WebElement):
    num_ratings = element.find_element(
        By.CSS_SELECTOR, ".page_charts_section_charts_item_details_ratings .full"
    )
    num_ratings = int(num_ratings.text.strip().replace(",", ""))
    return num_ratings


def get_album_num_reviews(element: WebElement):
    num_reviews = element.find_element(
        By.CSS_SELECTOR, ".page_charts_section_charts_item_details_reviews .full"
    )
    num_reviews = int(num_reviews.text.strip().replace(",", ""))
    return num_reviews


def get_album_release_date(element: WebElement):
    release_date = element.find_element(
        By.CSS_SELECTOR, ".page_charts_section_charts_item_date > span:not([class])"
    )
    return release_date.text


def get_album_primary_genres(element: WebElement):
    genre_list = [
        element.text
        for element in element.find_elements(
            By.CSS_SELECTOR, ".page_charts_section_charts_item_genres_primary > .genre"
        )
    ]
    return genre_list


def get_album_secondary_genres(element: WebElement):
    genre_list = [
        element.text
        for element in element.find_elements(
            By.CSS_SELECTOR,
            ".page_charts_section_charts_item_genres_secondary > .genre",
        )
    ]
    return genre_list


def get_album_average_score(element: WebElement):
    average_score = element.find_element(
        By.CLASS_NAME, "page_charts_section_charts_item_details_average_num"
    )
    average_score = Decimal(average_score.text.strip())
    return average_score


def get_album_top_descriptors(element: WebElement):
    descriptors = [
        element.text
        for element in element.find_elements(
            By.CSS_SELECTOR,
            ".page_charts_section_charts_item_genre_descriptors > .comma_separated",
        )
    ]
    return descriptors


def get_album_rym_href(element: WebElement):
    rym_url = element.find_element(
        By.CLASS_NAME, "page_charts_section_charts_item_link"
    ).get_attribute("href")
    return rym_url


def generate_album_data(elements: List[WebElement]):
    list = []
    for element in elements:
        rank = get_album_rank(element)
        title = get_album_name(element)
        artists = get_album_artists(element)
        num_ratings = get_album_num_ratings(element)
        average_score = get_album_average_score(element)
        num_reviews = get_album_num_reviews(element)
        release_date = get_album_release_date(element)
        primary_genres = get_album_primary_genres(element)
        secondary_genres = get_album_secondary_genres(element)
        descriptors = get_album_top_descriptors(element)
        rym_href = get_album_rym_href(element)
        list.append(
            Album(
                rank,
                title,
                artists,
                average_score,
                num_ratings,
                num_reviews,
                release_date,
                primary_genres,
                secondary_genres,
                descriptors,
                rym_href,
            )
        )
        print(f"Created \"{title}\" album object")

    return list


if __name__ == "__main__":
    elements = get_rym_top_albums_data()
    list = generate_album_data(elements)
    save_albums_data_to_csv(*list)
