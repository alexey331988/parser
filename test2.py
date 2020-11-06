import requests
from bs4 import BeautifulSoup
import csv
import os
import random
from time import sleep

URL = 'https://m.habr.com/ru/top/weekly/'

HOST = 'https://m.habr.com'

HEADERS = {
    "Accept": "*/*",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.102 Mobile Safari/537.36 '
}

FILE = 'article.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# def get_pages_count(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     pagination = soup.find_all('a', id='pagination-next-page')
#     print(pagination)

    # page = html.find('a', id='pagination-next-page')


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='tm-articles-list__item tm-hot-nav')

    article = []

    for item in items:
        article.append({
            'title': item.find('h2', class_='tm-article-snippet__title').get_text(strip=True),
            'link': HOST + item.find('a', class_='tm-article-snippet__title-link').get('href'),
            'user_name': item.find('a', class_='tm-user-info__username').get_text(strip=True),
            'user_link': HOST + item.find('a', class_='tm-user-info__username').get('href'),
               })
    print(article)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        # pages_count = get_pages_count(html.text)
        article = get_content(html.text)

    else:
        print('Error')

parse()