def get_subscriptions_for_user(user_id):
    return f"""
            SELECT anime_id, dubbing_id, title, studio FROM subscription
                INNER JOIN anime USING(anime_id)
                INNER JOIN dubbing USING(dubbing_id)
            WHERE user_id = {user_id};
            """


def get_copy_subscription(user_id, dub_id, anime_id):
    return f"""SELECT * FROM subscription 
               WHERE user_id={user_id} AND dubbing_id={dub_id} AND anime_id={anime_id};
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


def get_all_from_users():
    return 'SELECT user_id FROM users'


def add_user(user_id):
    return f"""
            INSERT INTO users (user_id)
            VALUES ({user_id});
            """


def insert_into_mail(user_id, mail):
    return f"""INSERT INTO mail
               VALUES({user_id}, '{mail['title']}', '{mail['episode']}', '{mail['studio']}')
            """


def get_mails(user_id):
    f"""SELECT title, episode, studio FROM mail
        WHERE user_id = {user_id}
     """


def delete_from_table(table):
    return f"""DELETE FROM {table}
            """


def add_new_anime(anime):
    return f"""INSERT INTO anime (title)
                     VALUES ('{anime}')
            """
