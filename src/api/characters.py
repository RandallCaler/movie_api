from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """
    for character in db.characters:
        if character["character_id"] == id:
            print("character found")

    #for 
     #top_conversations.append(conversation)

    row = None
    for character in db.characters:
      if character["character_id"] == id:
        row=character

    if row is None:
      raise HTTPException(status_code=404, detail="movie not found.")
      
    top_convos = []
    for dialogue in db.conversations:
      if(dialogue["character1_id"]==id or dialogue["character2_id"]==id):
        top_convos.append(dialogue)

    line_list = []  
    for conversation in top_convos:
      count = 0
      for line in db.lines:
        if(line["conversation_id"]==conversation["conversation_id"]):
          count+=1
      line_list.append(conversation, count)
    line_list.sort(key=[1])

    convo_list = []
    for convo in line_list:
      convo_json = {
        "character_id" : convo["character_id"],
        "character" : convo["character"],
        "gender" : convo["gender"],
        "number_of_lines_together" : convo["number_of_lines_together"]
      }
      convo_list.append(convo_json)
      

    json = {
      "character_id" : row["character_id"],
      "character" : row["character"],
      "movie" : row["movie"],
      "gender" : row["gender"],
      "top_conversations" : convo_list
    }

    return json


class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: character_sort_options = character_sort_options.character,
):
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    characterList = []
    if(name is ""):
      for character in db.characters:
        characterList.append(character)
    else:
      for character in db.characters:
        if character["name"] == name:
          characterList.append(character)

    if sort == character_sort_options.character:
      characterList.sort(key=lambda c: (c["name"]))
    elif sort == character_sort_options.movie:
      characterList.sort(key=lambda c: (c["title"]))
    elif sort == character_sort_options.number_of_lines:
      characterList.sort(key=lambda c: (c["number_of_lines"]))
      characterList.reverse()
    else:
       raise AssertionError("not sorted")

    json = {
      {
        "character_id": int(m["character_id"]),
        "character": m["name"],
        "movie" : m["movie_id"],
        "number_of_lines" : float(m["number_of_lines"]),
       }
       for m in characterList[offset : offset + limit]
    }
    return json
