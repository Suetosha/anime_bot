from database.db_connection import get_from_db, add_to_db
import re
from constants.queries import get_id_dubbing, add_to_subscription, get_copy_subscription


def get_anime_list(query, anime_title):
    anime_list = list(map(lambda row: (row['anime_id'], row['title'].lower()), get_from_db(query)))
    r = re.compile(f".*{anime_title}")
    new_list = list(filter(lambda row: re.match(r, row[1]), anime_list))
    new_list = [(id, title.capitalize()) for id, title in new_list]

    return new_list


def add_all_dubbing(user_id, title_id):
    dubbing_id = get_from_db(get_id_dubbing())
    filtered_dub_id = list(filter(lambda d: not get_from_db(get_copy_subscription(user_id, d['dubbing_id'], title_id)), dubbing_id))
    for dub in filtered_dub_id:
        add_to_db(add_to_subscription(user_id, dub['dubbing_id'], title_id))
    return filtered_dub_id


def add_dubbing(user_id, dub_id, title_id):
    request = add_to_subscription(user_id, dub_id, title_id)
    add_to_db(request)