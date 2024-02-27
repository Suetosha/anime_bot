from bs4 import BeautifulSoup
import requests
from database.db_connection import get_from_db, add_to_db
from constants.queries import get_mails, get_subscriptions_for_user, insert_into_mail, \
    get_all_from_users, add_new_anime, delete_from_table
from aiogram import Bot
from datetime import datetime
from aiogram import md

animego_url = 'https://animego.org'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
anti_ddos_cookie_key = '__ddg1_'
anti_ddos_cookie_file_name = '../anti_ddos_cookie.txt'


def set_anti_ddos_cookie(value):
    with open(anti_ddos_cookie_file_name, 'w') as f:
        f.write(value)


def get_anti_ddos_cookie():
    value = ''
    with open(anti_ddos_cookie_file_name, 'w+') as f:
        value = f.read().strip()
    return value


def get_request(url):
    session = requests.Session()
    session.headers.update({'user-agent': user_agent})
    session.cookies.set(anti_ddos_cookie_key, get_anti_ddos_cookie())

    res = session.get(url)
    anti_ddos_cookie = res.cookies.get_dict().get(anti_ddos_cookie_key, '')

    if res.status_code == 500:
        set_anti_ddos_cookie(anti_ddos_cookie)
        session.cookies.set(anti_ddos_cookie_key, get_anti_ddos_cookie())

        res = session.get(url)

    return res


def get_resent_anime(year, season):
    current_anime = []
    page = 1

    while True:
        url = f'{animego_url}/anime/season/{year}/{season}?page={page}'
        response = get_request(url)
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
    response = get_request(animego_url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_lists = soup.findAll('div', class_='card')[0]
    today_updates = all_lists.find('div', class_='last-update-container')

    today_updates_urls = [upd['onclick'] for upd in today_updates]
    today_updates_urls = list(map(lambda url: url.split("'")[1], today_updates_urls))

    today_updates_info = today_updates.findAll('div', class_='text-right')
    today_updates_info = list(map(lambda data: list(data.children), today_updates_info))

    today_updates_series = list(map(lambda data: data[0].string, today_updates_info))
    today_updates_dub = list(map(lambda data: data[1].string.replace('(', '').replace(')', '').capitalize(), today_updates_info))

    today_update_titles = today_updates.findAll('span', class_='last-update-title')
    today_update_titles = list(map(lambda data: data.text, today_update_titles))

    today_updates = list(zip(today_update_titles, today_updates_series, today_updates_dub, today_updates_urls))

    today_updates = [{'title': title, 'episode': episode, 'studio': studio, 'url': url}
                     for title, episode, studio, url in today_updates]

    return today_updates


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
    anime_updates = get_new_updates()
    users = get_from_db(get_all_from_users())

    for user in users:
        updates = get_update_list(user['user_id'], anime_updates)
        await bot.send_message(user['user_id'], updates)


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


