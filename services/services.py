from db_connection import get_from_db
import re


def get_anime_list(query, anime_title):
    anime_list = list(map(lambda row: (row['anime_id'], row['title'].lower()), get_from_db(query)))
    r = re.compile(f".*{anime_title}")
    new_list = list(filter(lambda row: re.match(r, row[1]), anime_list))
    new_list = [(id, title.capitalize()) for id, title in new_list]

    return new_list
