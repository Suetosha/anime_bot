from database.db_connection import get_from_db, add_to_db
from constants.queries import get_mails, get_subscriptions_for_user, insert_into_mail, \
    get_all_from_users, add_new_anime, delete_from_table, get_mailing_status
from aiogram import Bot
from datetime import datetime
from services.parser import get_new_updates, get_resent_anime


def get_update_list(user_id, anime_updates):
    updates = []

    sent_mails = get_from_db(get_mails(user_id))
    user_subscriptions = get_from_db(get_subscriptions_for_user(user_id))

    for user_subscription in user_subscriptions:
        for anime_update in anime_updates:
            if user_subscription['title'] == anime_update['title'] \
                    and user_subscription['studio'] == anime_update['studio']:
                updates.append(anime_update)

    if sent_mails:
        def filter_updates(update):
            upd = update.copy()
            del upd['url']
            return upd not in sent_mails

        updates = list(filter(filter_updates, updates))

    if updates:
        for update in updates:
            add_to_db(insert_into_mail(user_id, update))

        updates = [f"Вышло: {anime['title']} {anime['episode']} в озвучке {anime['studio']}\n" +
                   f"<a href = \"https://animego.org{anime['url']}\"> Смотреть </a>"
                   for anime in updates]

        updates = '\n\n'.join(updates)
        return updates


async def send_updates(bot: Bot):
    updates = []
    anime_updates = get_new_updates()
    users = get_from_db(get_all_from_users())

    for user in users:
        user_id = user['user_id']
        mailing_status = get_from_db(get_mailing_status(user_id))[0]['sending_messages']
        updates = get_update_list(user_id, anime_updates)

        if mailing_status and updates:
            await bot.send_message(user_id, updates)


def send_updates_now(user_id):
    anime_updates = get_new_updates()
    updates = get_update_list(user_id, anime_updates)
    return updates


def get_new_anime(num):
    year = datetime.now().year
    months = {1: 'winter', 4: 'spring', 7: 'summer', 10: 'fall'}
    animes = get_resent_anime(year, months[num])

    for anime in animes:
        query = add_new_anime(anime)
        add_to_db(query)


def clean_up_table():
    return add_to_db(delete_from_table('mail'))
