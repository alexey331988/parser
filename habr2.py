import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import OperationalError
import time
import random

host = 'https://m.habr.com'
URL = 'https://m.habr.com/ru/hub/infosecurity'

headers = {
    "Accept": "*/*",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.135 Mobile Safari/537.36 '
}


def get_html(url):
    req = requests.get(url, headers=headers)
    return req


def get_content(html):
    projects_data_list = []

    soup = BeautifulSoup(html, 'lxml', )
    articles = soup.find_all('article', class_='tm-articles-list__item')

    project_urls = []

    for article in articles:
        project_url = host + article.find('a', class_='tm-article-snippet__title-link').get('href')
        project_urls.append(project_url)

    count = 0
    for project_url in project_urls:
        req = requests.get(project_url, headers)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')

        try:
            date = soup.find('span', class_='tm-article-snippet__datetime-published').get('title')
        except Exception:
            date = 'No date'

        try:
            name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
            if name:
                name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
            else:
                name = 'Имя не указано'
        except Exception:
            name = 'No name'

        try:
            nick_name = soup.find('a', class_='tm-user-snippet__nickname').get_text(strip=True)
        except Exception:
            nick_name = 'No nick name'

        try:
            name_link = host + soup.find('a', class_='tm-user-snippet__title').get('href')
        except Exception:
            name_link = 'No name link'

        try:
            title = soup.find('h1', class_='tm-article-snippet__title').get_text(strip=True)
        except Exception:
            title = 'No title'

        try:
            text = soup.find('div', id='post-content-body').get_text(strip=True)
        except Exception:
            text = 'No text'

        projects_data_list.append((date, name, nick_name, name_link, title, project_url, text))

        count += 1
        print(f'#{count}: {project_url}: is done!')
        time.sleep(random.randrange(2, 4))

    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""CREATE TABLE projects_data_list
                          (Date text, Author_name text, Nick_name text, Link_to_the_author text, 
                           Article_title text, Link_to_the_article text, Text_of_article text)
                       """)
    except OperationalError:
        pass

    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS Article_title ON projects_data_list (Article_title)")

    cursor.executemany('INSERT OR IGNORE INTO projects_data_list VALUES (?,?,?,?,?,?,?)', projects_data_list)
    conn.commit()
    conn.close()


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
