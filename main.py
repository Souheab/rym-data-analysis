from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import os


class Album:
    def __init__(self, rank: int, title: str, artists: List[str]):
        self.rank = rank
        self.title = title
        self.artists = artists

    def __repr__(self):
        return f"[{self.rank}, {self.title}, {self.artists}]"

    def __str__(self):
        return self.__repr__()


def get_rym_top_albums_data(page=1, driver=webdriver.Chrome()):
    #    driver.get(f"https://rateyourmusic.com/charts/top/album/all-time/{page}/")
    #    driver.implicitly_wait(3)
    file_path = os.path.abspath("./mock.html")
    driver.get(f"file://{file_path}")
    elements = driver.find_elements(By.CLASS_NAME, "page_section_charts_item_wrapper")
    return elements


def get_element_rank(element: WebElement):
    element_id = element.get_attribute("id")
    return int(element_id[3:])


def get_element_album_name(element: WebElement):
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


def get_score(element: WebElement):
    pass


def get_num_ratings(element: WebElement):
    pass


def get_num_reviews(element: WebElement):
    pass


def generate_album_data(elements: List[WebElement]):
    list = []
    for element in elements:
        rank = get_element_rank(element)
        title = get_element_album_name(element)
        artists = get_album_artists(element)
        list.append(Album(rank, title, artists))

    return list


if __name__ == "__main__":
    elements = get_rym_top_albums_data()
    list = generate_album_data(elements)
    print(list)
