import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://arhangelsk.bezformata.com/'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                     'application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36'
           }
FILE = 'news.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='fourtopicbox')
    news = []
    for item in items:
        news.append({
            'link': item.find('a').get('href'),
            'date': item.find('meta', itemprop='datePublished').get('content'),
            'author': item.find('meta', itemprop='author').get('content'),
            'title': item.find('a').get('title'),
            'description': item.find('span', itemprop='description').get_text(strip=True)
        })
    return news


def save(items, path):
    with open(path, 'w', encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Ссылка', 'Дата аубликации', 'Автор нововсти', 'Заголовок новости', 'Краткое описание'])
        for item in items:
            writer.writerow([item['link'], item['date'], item['author'], item['title'], item['description']])



def parser():
    news = []
    for page in range(1, 31, 1):
        print(f'Парсинг страницы {page} из {30}...')
        link = '/science/?npage=' + str(page)
        html = get_html(URL, params = {'path': link})
        news.extend(get_content(html.text))
    save(news, FILE)
    print(f'Сохранено {len(news)} новостей')


parser()

