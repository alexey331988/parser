import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import asyncio
import random
from time import sleep

url = 'https://m.habr.com/ru/hub/infosecurity/'
# url = input('Введите ссылку на хаб: ')
host = 'https://m.habr.com'

HEADERS = {
    "Accept": "*/*",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'
}

response = requests.get(url, headers=HEADERS)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

container = soup.find('div', class_='tm-page__main')

article = container.find_all('article', class_='tm-articles-list__item')

urls = []
for a in article:
    url = host + a.find('a', class_='tm-article-snippet__title-link').get('href')
    urls.append(url)

urls_data = []

for url in urls:
    response = requests.get(url, headers=HEADERS)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    data = soup.find('span', class_='tm-article-snippet__datetime-published').get_text(strip=True)
    name = soup.find('a', class_='tm-user-snippet__title').get_text(strip=True)
    nick_name = soup.find('a', class_='tm-user-snippet__nickname').get_text(strip=True)
    name_link = host + soup.find('a', class_='tm-user-snippet__title').get('href')
    title = soup.find('h1', class_='tm-article-snippet__title').get_text(strip=True)
    text = soup.find('div', id='post-content-body').get_text(strip=True)

    urls_data.append((data, name, nick_name, name_link, title, text))


urls_urlsdata = [(u, *d) for u, d in zip(urls, urls_data)]

# print(urls_urlsdata)


# sleep(random.randrange(3, 6))


conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

#Создание таблицы
cursor.execute("""CREATE TABLE urls_data
                  (url text, data text, name text, nick_name text,
                   name_link text, title text, text text)
               """)

cursor.executemany("INSERT INTO urls_data VALUES (?,?,?,?,?,?,?)", urls_urlsdata)
conn.commit()
