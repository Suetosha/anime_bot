from bs4 import BeautifulSoup
from services.animego_request import animego_url, get_request


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
    today_updates_dub = list(map(lambda data:
                                 data[1].string.replace('(', '').replace(')', '').capitalize(),
                                 today_updates_info))

    today_update_titles = today_updates.findAll('span', class_='last-update-title')
    today_update_titles = list(map(lambda data: data.text, today_update_titles))

    today_updates = list(zip(today_update_titles, today_updates_series, today_updates_dub, today_updates_urls))

    today_updates = [{'title': title, 'episode': episode, 'studio': studio, 'url': url}
                     for title, episode, studio, url in today_updates]

    return today_updates


