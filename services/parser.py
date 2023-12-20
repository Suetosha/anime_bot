from bs4 import BeautifulSoup
import requests


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



get_resent_anime(2023, 'fall')

def get_new_updates():
    url = 'https://animego.org/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    all_lists = soup.findAll('div', class_='card')[0]
    today_updates = all_lists.find('div', class_='last-update-container')
    today_updates_info = today_updates.findAll('div', class_='text-right')

    today_updates_info = list(map(lambda data: list(data.children), today_updates_info))

    today_updates_series = list(map(lambda data: data[0].string, today_updates_info))
    today_updates_dub = list(map(lambda data: data[1].string, today_updates_info))

    today_update_titles = today_updates.findAll('span', class_='last-update-title')
    today_update_titles = list(map(lambda data: data.text, today_update_titles))

    today_updates = list(zip(today_update_titles, today_updates_series, today_updates_dub))

    return today_updates
