def get_from_subscription(user_id):
    return f"""
            SELECT anime_id, dubbing_id, title, studio FROM subscription
                INNER JOIN anime USING(anime_id)
                INNER JOIN dubbing USING(dubbing_id)
            WHERE user_id = {user_id};
            """


def get_copy_subscription(user_id, dub_id, anime_id):
    f"""SELECT * FROM subscription 
               WHERE user_id={user_id} AND dubbing_id={dub_id} AND anime_id={anime_id}
     """


def delete_from_subscription(user_id, dub_id, anime_id):
    return f"""
            DELETE FROM subscription
            WHERE user_id = {user_id} AND dubbing_id = {dub_id} AND anime_id = {anime_id};
            """


def add_to_subscription(user_id, dub_id, anime_id):
    return f"""
            INSERT INTO subscription (user_id, dubbing_id, anime_id)
            VALUES ({user_id}, {dub_id}, {anime_id});
            """


def get_from_table(table_name):
    return f"""SELECT * FROM {table_name}"""


def get_from_users(user_id):
    return f"""SELECT * FROM users 
               WHERE user_id='{user_id}'
            """


def add_user(user_id):
    return f"""
            INSERT INTO users (user_id)
            VALUES ({user_id});
            """
