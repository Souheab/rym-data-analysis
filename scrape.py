from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
from decimal import Decimal
import pandas as pd
import time
import random
import os
from bs4 import BeautifulSoup


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


def get_rym_top_albums_mock_html_source():
    with open("mock.html", "r", encoding="utf-8") as file:
        html_source = file.read()

    return html_source


def get_rym_top_albums_html_source(driver, page=1):
    driver.get(f"https://rateyourmusic.com/charts/top/album/all-time/{page}/")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "page_section_charts_item_wrapper")
            )
        )
    except TimeoutException:
        print("Timeout while waiting for page to load")
        return []

    html_source = driver.page_source
    driver.get("about:blank")
    return html_source


def get_rym_top_albums_elements(html_source: str):
    soup = BeautifulSoup(html_source, "html.parser")
    elements = soup.find_all("div", class_="page_section_charts_item_wrapper")
    return elements


def get_album_rank(element) -> int:
    element_id = element.get("id")
    return int(element_id[3:])


def get_album_name(element) -> str:
    album_name_parent_element = element.find(
        "div", class_="page_charts_section_charts_item_title"
    )
    return album_name_parent_element.text.strip()


def get_album_artists(element) -> List[str]:
    album_artists_parent_elements = element.find_all("a", class_="artist")
    album_artists_names = [
        el.text[:-1].strip() if el.text.endswith("&") else el.text.strip()
        for el in album_artists_parent_elements
    ]
    return album_artists_names


def get_album_num_ratings(element) -> int:
    num_ratings_element = element.select_one(
        ".page_charts_section_charts_item_details_ratings .full"
    )
    return int(num_ratings_element.text.strip().replace(",", ""))


def get_album_num_reviews(element) -> int:
    try:
        num_reviews_element = element.select_one(
            ".page_charts_section_charts_item_details_reviews .full"
        )
        return int(num_reviews_element.text.strip().replace(",", ""))
    except:
        # There might be no reviews which will raise an exception, so return 0
        return 0


def get_album_release_date(element) -> str:
    release_date_element = element.select_one(
        ".page_charts_section_charts_item_date > span:not([class])"
    )
    return release_date_element.text.strip()


def get_album_primary_genres(element) -> List[str]:
    genre_elements = element.select(
        ".page_charts_section_charts_item_genres_primary > .genre"
    )
    return [el.text.strip() for el in genre_elements]


def get_album_secondary_genres(element) -> List[str]:
    genre_elements = element.select(
        ".page_charts_section_charts_item_genres_secondary > .genre"
    )
    return [el.text.strip() for el in genre_elements]


def get_album_average_score(element) -> Decimal:
    average_score_element = element.find(
        "span", class_="page_charts_section_charts_item_details_average_num"
    )
    return Decimal(average_score_element.text.strip())


def get_album_top_descriptors(element) -> List[str]:
    descriptor_elements = element.select(
        ".page_charts_section_charts_item_genre_descriptors > .comma_separated"
    )
    return [el.text.strip() for el in descriptor_elements]


def get_album_rym_href(element) -> str:
    rym_url_element = element.find("a", class_="page_charts_section_charts_item_link")
    return rym_url_element.get("href")


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
        album = Album(
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
        print(f'Created "{title}" album object')
        list.append(album)

    return list


if __name__ == "__main__":
    for i in range(38, 40):
        # Have to recreate the driver every time to not get blocked
        driver = webdriver.Chrome()
        driver.implicitly_wait(1)
        print(f"Getting data from page {i}")
        html_source = get_rym_top_albums_html_source(driver, i)
        driver.quit()
        elements = get_rym_top_albums_elements(html_source)
        list = generate_album_data(elements)
        save_albums_data_to_csv(*list)
        print(f"Page {i} written to CSV file.")
        sleep_time = random.uniform(1, 3)
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
