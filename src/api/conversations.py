from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """

    movie = db.movies.get(movie_id)
    count=1
    if movie:
        char1=db.characters.get(conversation.character_1_id)
        char2=db.characters.get(conversation.character_2_id)
        #lines=conversation.lines
        if char1==char2:
            raise HTTPException(status_code=422, detail="characters are the same.")
        elif db.characters.get(char1.movie_id)!=movie_id:
            raise HTTPException(status_code=422, detail="character1 does not exist.")
        elif db.characters.get(char2.movie_id)!=movie_id:
            raise HTTPException(status_code=422, detail="character2 does not exist.")
        else:
            #if line.character_id==char1.character_id or line.character_id==char2.character_id:
            db.lines.get(movie_id).line_sort=count
            db.last_convo_id+=1
            db.conversations.append({"conversation_id": db.last_convo_id, "movie_id": movie_id, "character1_id":conversation.character_1_id, "character2_id":conversation.character_2_id})
            db.upload_new_log(["conversation_id","character1_id","character2_id","movie_id"], db.conversations, "conversations.csv")
            for line in conversation.lines:
                db.last_line_id+=1
                db.lines.append({"character_id":line.character_id, "line_text":line.line_text, "line_id":db.last_line_id, "conversation_id":db.last_convo_id, "line_sort":count})
                count+=1
            db.upload_new_log(["line_id","character_id","movie_id","conversation_id","line_sort","line_text"], db.lines, "lines.csv")
        

    # TODO: Remove the following two lines. This is just a placeholder to show
    # how you could implement persistent storage.

    # print(conversation)
    # db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    # db.upload_new_log()
