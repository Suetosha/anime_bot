from bs4 import BeautifulSoup
import requests
from db_connection import get_from_db, add_to_db
from constants import queries
from aiogram import Bot
from datetime import datetime


def get_resent_anime(year, season):
    current_anime = []
    page = 1

    while True:
        url = f'https://animego.org/anime/season/{year}/{season}?page={page}'
        response = requests.get(url)
        print(response)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        all_lists = soup.findAll('div', class_='animes-list-item')
        lists = list(map(lambda data: data.find('div', class_='media-body'), all_lists))
        anime = list(map(lambda data: data.find('a').text, lists))
        current_anime.extend(anime)
        page += 1

    return current_anime


def get_new_updates():
    url = 'https://animego.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_lists = soup.findAll('div', class_='card')[0]
    today_updates = all_lists.find('div', class_='last-update-container')
    today_updates_info = today_updates.findAll('div', class_='text-right')

    today_updates_info = list(map(lambda data: list(data.children), today_updates_info))

    today_updates_series = list(map(lambda data: data[0].string, today_updates_info))
    today_updates_dub = list(map(lambda data: data[1].string, today_updates_info))

    today_update_titles = today_updates.findAll('span', class_='last-update-title')
    today_update_titles = list(map(lambda data: data.text, today_update_titles))

    today_updates = list(zip(today_update_titles, today_updates_series, today_updates_dub))

    today_updates = [{'title': title, 'episode': episode, 'studio': studio.replace('(', '').replace(')', '').capitalize()}
                     for title, episode, studio in today_updates]

    return today_updates


async def send_updates(bot: Bot):
    anime_updates = get_new_updates()
    users = get_from_db(queries.get_all_from_users())

    for user in users:
        updates = []

        sent_updates = get_from_db(queries.get_mails(user['user_id']))
        user_subscriptions = get_from_db(queries.get_subscriptions_for_user(user['user_id']))

        for user_subscription in user_subscriptions:
            for anime_update in anime_updates:
                if user_subscription['title'] == anime_update['title'] \
                        and user_subscription['studio'] == anime_update['studio']:
                    updates.append(anime_update)

        def filter_updates(update):
            return update not in sent_updates

        updates = list(filter(filter_updates, updates))

        if updates:

            for update in updates:
                add_to_db(queries.insert_into_mail(user['user_id'], update))

            updates = [f"Вышло: {anime['title']} {anime['episode']} в озвучке {anime['studio']}" for anime in
                                updates]

            await bot.send_message(user['user_id'], '\n\n'.join(updates))


def get_new_anime(num):
    year = datetime.now().year
    months = {1: 'winter', 4: 'spring', 7: 'summer', 10: 'fall'}
    animes = get_resent_anime(year, months[num])

    for anime in animes:
        query = queries.add_new_anime(anime)
        add_to_db(query)


def clean_up_table():
    return add_to_db(queries.delete_from_table('mail'))
