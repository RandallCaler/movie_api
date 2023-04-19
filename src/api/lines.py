from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db

router = APIRouter()


# def get_longest_conv(line):
#     l_id = line.id
#     movie_id = line.movie_id
#     all_convs = filter(
#         lambda conv: conv.movie_id == movie_id
#         and (conv.c1_id == l_id or conv.c2_id == l_id),
#         db.conversations.values(),
#     )
#     line_counts = Counter()

#     for conv in all_convs:
#         other_id = conv.c2_id if conv.c1_id == l_id else conv.c1_id
#         line_counts[other_id] += conv.num_lines

#     return line_counts.most_common()


@router.get("/lines/{id}", tags=["lines"])
def get_line(id: int):
    """
    This endpoint returns a single line by its identifier. For each line
    it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/line/{line_id}` endpoint.
    * `character`: The name of the character who says the line.
    * `movie`: The movie the line is from.
    * `text`: The gender of the character.
    """

    line = db.lines.get(id)

    if line:
        character = db.characters.get(line.c_id)
        movie = db.movies.get(line.movie_id)
        result = {
            "line_id": line.id,
            "character": character.name,
            "movie": movie and movie.title,
            "text": line.line_text,
            # "longest_conversations": (
            #     {
            #         "conversation_id": db.conversations[other_id].conversation_id,
            #         "movie": db.movies[other_id].title,
            #         "lines": lines,
            #     }
            #     for other_id, lines in get_longest_conv(line)
            # ),
        }
        return result

    raise HTTPException(status_code=404, detail="line not found.")


@router.get("/lines/conversations/{id}", tags=["conversations"])
def get_conversation(id:int):
    """
    This endpoint returns a single line by its identifier. For each line
    it returns:
    * `conversation_id`: the internal id of the line. Can be used to query the
      `conversation/{id}` endpoint.
    * `character1`: The name of the character who says the line.
    * `character2`: The movie the line is from.
    * `movie`: The movie the conversation is in.
    """
    conversation = db.conversations.get(id)
    if conversation:
        character1 = db.characters.get(conversation.character1_id)
        character2 = db.characters.get(conversation.character2_id)
        movie = db.movies.get(conversation.movie_id)
        result = {
            "conversation_id": conversation.id,
            "character1": character1.name,
            "character2": character2.name,
            "movie": movie and movie.title,
        }
        return result
    raise HTTPException(status_code=404, detail="conversation not found.")


class line_sort_options(str, Enum):
    movie = "movie"
    character = "character"
    conversation = "conversation"


@router.get("/lines/", tags=["lines"])
def list_lines(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: line_sort_options = line_sort_options.character,
):
    """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/line/{line_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the line is from.
    You can filter for characters whose name contains a string by using the
    `name` query parameter.
    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `conversation` - Sort by conversation_id, highest to lowest.
    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    if name:

        def filter_fn(l):
            return l.name and name.upper() in l.name

    else:

        def filter_fn(_):
            return True

    items = list(filter(filter_fn, db.lines.values()))

    def none_last(x, reverse=False):
        return (x is None) ^ reverse, x

    if sort == line_sort_options.character:
        items.sort(key=lambda l: none_last(db.characters[l.c_id].name))
    elif sort == line_sort_options.movie:
        items.sort(key=lambda l: none_last(db.movies[l.movie_id].title))
    elif sort == line_sort_options.conversation:
        items.sort(key=lambda l: none_last(db.conversations[l.conv_id].conversation_id))

    json = (
        {
            "line_id": l.id,
            "character": db.characters[l.c_id].name,
            "movie": db.movies[l.movie_id].title,
            "text": l.line_text,
        }
        for l in items[offset : offset + limit]
    )
    return json