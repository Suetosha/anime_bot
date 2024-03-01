import requests


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