import sqlite3
from sqlite3 import OperationalError

import requests
from bs4 import BeautifulSoup

url = 'https://m.habr.com/ru/hub/infosecurity/page' + str(1)
# url = 'https://m.habr.com/ru/hub/infosecurity/'
# url = input('Введите ссылку на хаб: ')
host = 'https://m.habr.com'

num_of_page = 2

HEADERS = {
    "Accept": "*/*",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.135 Mobile Safari/537.36 '
}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# def get_pages_count(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     pagination = soup.find('a', class_='page-item mhide')
#     if pagination:
#         return int(pagination[-1].get_text())
#     else:
#         return 1



def get_content(html):

    for i in range(num_of_page):
        # url = 'https://m.habr.com/ru/hub/infosecurity/page' + str(1)
        # response = requests.get(url, headers=HEADERS)
        # html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find_all('article', class_='tm-articles-list__item')
        urls = []
        for a in article:
            url = host + a.find('a', class_='tm-article-snippet__title-link').get('href')
            urls.append(url)

        # print(urls)

    # soup = BeautifulSoup(html, 'html.parser')
    # article = soup.find_all('article', class_='tm-articles-list__item')
    #
    # urls = []
    #
    # for a in article:
    #     url = host + a.find('a', class_='tm-article-snippet__title-link').get('href')
    #     urls.append(url)
    #


    urls_data = []
    count = 0
    for url in urls:
        response = requests.get(url, headers=HEADERS)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        date = soup.find('span', class_='tm-article-snippet__datetime-published').get('title')
        name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)

        if name:
            name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
        else:
            name = 'Имя не указано'

        nick_name = soup.find('a', class_='tm-user-snippet__nickname').get_text(strip=True)
        name_link = host + soup.find('a', class_='tm-user-snippet__title').get('href')
        title = soup.find('h1', class_='tm-article-snippet__title').get_text(strip=True)
        text = soup.find('div', id='post-content-body').get_text(strip=True)

        count += 1
        print(f'#{count}: {url}: is done!')

        urls_data.append((date, name, nick_name, name_link, title, text))

    urls_urlsdata = [(u, *d) for u, d in zip(urls, urls_data)]


def parse():
    html = get_html(url)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

parse()


# response = requests.get(url, headers=HEADERS)
# html = response.text
# soup = BeautifulSoup(html, 'html.parser')
# container = soup.find('div', class_='tm-page__main')
# article = container.find_all('article', class_='tm-articles-list__item')
#
# urls = []
#
#
#
# for a in article:
#     url = host + a.find('a', class_='tm-article-snippet__title-link').get('href')
#     urls.append(url)
#
# urls_data = []
#
# count = 0
# for url in urls:
#     response = requests.get(url, headers=HEADERS)
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     date = soup.find('span', class_='tm-article-snippet__datetime-published').get('title')
#     name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
#
#     if name:
#         name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
#     else:
#         name = 'Имя не указано'
#
#     nick_name = soup.find('a', class_='tm-user-snippet__nickname').get_text(strip=True)
#     name_link = host + soup.find('a', class_='tm-user-snippet__title').get('href')
#     title = soup.find('h1', class_='tm-article-snippet__title').get_text(strip=True)
#     text = soup.find('div', id='post-content-body').get_text(strip=True)
#
#     count += 1
#     print(f'#{count}: {url}: is done!')
#
#
#     urls_data.append((date, name, nick_name, name_link, title, text))
#
# urls_urlsdata = [(u, *d) for u, d in zip(urls, urls_data)]
#
# # print(urls_urlsdata)
#
#
# # sleep(random.randrange(3, 6))
#
#
# conn = sqlite3.connect("mydatabase.db")
# cursor = conn.cursor()
# # Создание таблицы
# try:
#     cursor.execute("""CREATE TABLE urls_data
#                       (url text, data text, name text, nick_name text,
#                        name_link text, title text, text text)
#                    """)
# except OperationalError:
#     var = None
#
# cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS url ON urls_data (url)")
#
# cursor.executemany("INSERT OR IGNORE INTO urls_data VALUES (?,?,?,?,?,?,?)", urls_urlsdata)
# conn.commit()
# conn.close()
