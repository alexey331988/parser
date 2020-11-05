import requests
from bs4 import BeautifulSoup
import csv
# import os

URL = 'https://auto.ria.com/newauto/marka-porsche/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



async def get_content(html):
    soup = await BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')
    cars = []

    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Цена в гривнах не указана'
        href = HOST + item.find('a').get('href')
        title = item.get_text(strip=True)
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(),
            'tech': item.find('div', class_='proposition_equip').get_text(),
            'link': href,
            'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('strong').get_text(),

        })

    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Комплектация', 'Ссылка', 'Цена в $', 'Цена в UAH', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['tech'], item['link'], item['usd_price'], item['uah_price'],
                             item['city']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        # get_content(html.text)
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
        # os.startfile(FILE)

    else:
        print('Error')


parse()
