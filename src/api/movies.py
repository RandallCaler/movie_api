from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


# include top 3 actors by number of lines
@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: str):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """

    for movie in db.movies:
        if movie["movie_id"] == movie_id:
            print("movie found")

    row = None
    for movie in db.movies:
      if movie["movie_id"] == movie_id:
        row=movie

    if row is None:
      raise HTTPException(status_code=404, detail="movie not found.")
    
    top_chars = []
    for line in db.lines:
        if line["movie_id"]==movie_id:
            top_chars.append(line)

    chars = []
    for character in top_chars:
        count = 1
        if(character["character_id"] not in chars):
            chars.append(character, count)
        else:
            chars.index(character["character_id"])[1]+=1

    chars.sort(key=[1])

    charac_list = chars
    for charac in row["top_characters"]:
      "character_id" : charac["character_id"]
      "character" : charac["character"]
      "num_lines" : charac["num_lines"]
      charac_list.append(charac)

    # charac_json = {
    #   charac_list
    # }

    json = {
        "movie_id" : row["movie_id"],
        "title" : row["title"],
        "top_characters" : charac_list
    }

    # if json is None:
    #     raise HTTPException(status_code=404, detail="movie not found.")

    return json


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    movieList = []
    if(name is ""):
      for movie in db.movies:
        movieList.append(movie)
    else:
      for movie in db.movies:
        if movie["movie_title"] == name:
          movieList.append(movie)

    if(sort is "movie_title"):
      movieList.sort(movie["movie_title"])
    if(sort is "year"):
      movieList.sort(movie["year"])
    if(sort is "rating"):
      movieList.sort(movie["imdb_rating"])

    json = {
        movieList[offset, limit]
    }

    return json
