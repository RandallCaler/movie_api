import csv
from src.datatypes import Character, Movie, Conversation, Line
import os
import io
from supabase import Client, create_client
import dotenv
from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy
import dotenv
import urllib.parse


# DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()
# supabase_api_key = os.environ.get("SUPABASE_API_KEY")
# supabase_url = os.environ.get("SUPABASE_URL")

# if supabase_api_key is None or supabase_url is None:
#     raise Exception(
#         "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
#     )

# supabase: Client = create_client(supabase_url, supabase_api_key)

# sess = supabase.auth.get_session()

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = urllib.parse.quote_plus(os.environ.get("POSTGRES_PASSWORD"))
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url())
metadata_obj = sqlalchemy.MetaData()
movies = sqlalchemy.Table("movies", metadata_obj, autoload_with=engine)
characters = sqlalchemy.Table("characters", metadata_obj, autoload_with=engine)
lines = sqlalchemy.Table("lines", metadata_obj, autoload_with=engine)
conversations = sqlalchemy.Table("conversations", metadata_obj, autoload_with=engine)

# TODO: Below is purely an example of reading and then writing a csv from supabase.
# You should delete this code for your working example.

# lines_csv = (
#     supabase.storage.from_("movie-api")
#     .download("lines.csv")
#     .decode("utf-8")
# )

# lines = []
# for row in csv.DictReader(io.StringIO(lines_csv), skipinitialspace=True):
#     lines.append(row)
# last_line_id=row["line_id"]

# conversations_csv = (
#     supabase.storage.from_("movie-api")
#     .download("conversations.csv")
#     .decode("utf-8")
# )

# conversations = []
# for row in csv.DictReader(io.StringIO(conversations_csv), skipinitialspace=True):
#     conversations.append(row)
# last_convo_id=row["conversation_id"]

# # START PLACEHOLDER CODE

# # Reading in the log file from the supabase bucket


# # Writing to the log file and uploading to the supabase bucket
# def upload_new_log(headers, dictionary, filename):
#     output = io.StringIO()
#     csv_writer = csv.DictWriter(
#         output, fieldnames=headers
#     )
#     csv_writer.writeheader()
#     csv_writer.writerows(dictionary)
#     supabase.storage.from_("movie-api").upload(
#         filename,
#         bytes(output.getvalue(), "utf-8"),
#         {"x-upsert": "true"},
#     )


# # END PLACEHOLDER CODE


# def try_parse(type, val):
#     try:
#         return type(val)
#     except ValueError:
#         return None


# with open("movies.csv", mode="r", encoding="utf8") as csv_file:
#     movies = {
#         try_parse(int, row["movie_id"]): Movie(
#             try_parse(int, row["movie_id"]),
#             row["title"] or None,
#             row["year"] or None,
#             try_parse(float, row["imdb_rating"]),
#             try_parse(int, row["imdb_votes"]),
#             row["raw_script_url"] or None,
#         )
#         for row in csv.DictReader(csv_file, skipinitialspace=True)
#     }

# with open("characters.csv", mode="r", encoding="utf8") as csv_file:
#     characters = {}
#     for row in csv.DictReader(csv_file, skipinitialspace=True):
#         char = Character(
#             try_parse(int, row["character_id"]),
#             row["name"] or None,
#             try_parse(int, row["movie_id"]),
#             row["gender"] or None,
#             try_parse(int, row["age"]),
#             0,
#         )
#         characters[char.id] = char

# with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
#     conversations = {}
#     for row in csv.DictReader(csv_file, skipinitialspace=True):
#         conv = Conversation(
#             try_parse(int, row["conversation_id"]),
#             try_parse(int, row["character1_id"]),
#             try_parse(int, row["character2_id"]),
#             try_parse(int, row["movie_id"]),
#             0,
#         )
#         conversations[conv.id] = conv

# with open("lines.csv", mode="r", encoding="utf8") as csv_file:
#     lines = {}
#     for row in csv.DictReader(csv_file, skipinitialspace=True):
#         line = Line(
#             try_parse(int, row["line_id"]),
#             try_parse(int, row["character_id"]),
#             try_parse(int, row["movie_id"]),
#             try_parse(int, row["conversation_id"]),
#             try_parse(int, row["line_sort"]),
#             row["line_text"],
#         )
#         lines[line.id] = line
#         c = characters.get(line.c_id)
#         if c:
#             c.num_lines += 1

#         conv = conversations.get(line.conv_id)
#         if conv:
#             conv.num_lines += 1
