from album import Album
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import plotly.express as px


def load_albums_from_csv(
    num_albums=None,
    file_path="albums.csv",
) -> List[Album]:
    df = pd.read_csv(file_path, nrows=num_albums)
    albums_data = df.to_dict(orient="records")
    albums = [Album.from_dict(data) for data in albums_data]
    return albums


def analyze_highest_primary_genres(albums: List[Album]):
    primary_genres = {}
    for album in albums:
        for genre in album.primary_genres:
            if genre in primary_genres:
                primary_genres[genre] += 1
            else:
                primary_genres[genre] = 1

    sorted_genres = sorted(primary_genres.items(), key=lambda x: x[1], reverse=True)
    return sorted_genres


def plot_genres_histogram(sorted_genres: List[tuple]):
    genres, counts = zip(*sorted_genres)
    plt.bar(genres, counts)
    plt.xticks(rotation=90)
    plt.show()


def plot_genres_histogram_interactive(sorted_genres: List[tuple]):
    genres = [genre for genre, count in sorted_genres]
    counts = [count for genre, count in sorted_genres]

    df = pd.DataFrame({"Primary Genres": genres, "Number of Albums": counts})

    fig = px.bar(
        df,
        x="Primary Genres",
        y="Number of Albums",
        title="Number of Albums by Primary Genre",
    )
    fig.show()


if __name__ == "__main__":
    albums = load_albums_from_csv(1000)
    print(albums)
    genres = analyze_highest_primary_genres(albums)
    print(genres)
    plot_genres_histogram_interactive(genres)
