import requests  # Импортируем библиотеку для выполнения HTTP-запросов
from bs4 import BeautifulSoup as BS  # Импортируем библиотеку для парсинга HTML-кода
import re  # Импортируем библиотеку для работы с регулярными выражениями
import pandas as pd  # Импортируем библиотеку для работы с данными в виде таблицы
from datetime import datetime  # Импортируем класс datetime из библиотеки datetime

def main():
    data = {'Author': [], 'Date': [], 'Title': [], 'Text': [], 'Views': []}  # Создаем словарь для хранения данных
    df = pd.DataFrame(data)  # Создаем DataFrame для хранения данных в виде таблицы
    with open('links.txt', 'r') as f:  # Открываем файл с ссылками на статьи для чтения
        for line in f:  # Итерируемся по каждой строке файла
            print(line)  # Выводим текущую строку в консоль (для отладки)
            try:
                main_link = line.strip()  # Удаляем лишние пробелы и сохраняем ссылку на статью
                response = requests.get(main_link)  # Получаем содержимое страницы по указанной ссылке
                html = response.content  # Получаем HTML-код страницы
                soup = BS(html, "html.parser")  # Создаем объект BeautifulSoup для парсинга HTML

                Author = soup.find('span', {'class': 'tm-user-info tm-article-snippet__author'}).find('a', {'class': 'tm-user-info__username'}).text.strip()  # Извлекаем автора статьи

                datetime_str = soup.find('span', {'class': 'tm-article-datetime-published'}).find('time').get('datetime')  # Получаем строку с датой и временем публикации
                datetime_obj = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))  # Преобразуем строку в объект datetime
                Date = datetime_obj.strftime("%d.%m.%y")  # Форматируем дату

                Title = soup.find('h1', {'class': 'tm-title tm-title_h1'}).find('span').text.strip()  # Извлекаем заголовок статьи

                Text = soup.find('div', {'id': 'post-content-body'}).text.strip()  # Извлекаем текст статьи

                Views = soup.find('span', {'class': 'tm-icon-counter__value'}).text.strip()  # Извлекаем количество просмотров статьи

                new_data = {'Author': [Author], 'Date': [Date], 'Title': [Title], 'Text': [Text], 'Views': [Views]}  # Создаем новую запись данных
                new_df = pd.DataFrame(new_data)  # Создаем DataFrame для новой записи
                df = pd.concat([df, new_df], ignore_index=True)  # Объединяем новую запись с общим DataFrame
            except:
                print(f'Error: {main_link}')  # Выводим сообщение об ошибке в случае исключения

    df.to_csv('dataset.csv', index=False)  # Сохраняем DataFrame в CSV файл

# Функция для получения страниц каталога статей
def get_links():
    main_link = "https://habr.com/ru/companies/ru_mts/articles/"  # Задаем основную ссылку на каталог статей
    pages = 1  # Задаем количество доступных страниц
    iter = 1  # Инициализируем итератор
    run = True
    while run:  # Запускаем цикл прохода по страницам каталога статей
        if iter == pages:  # Проверяем условие остановки цикла
            run = False
        response = requests.get(f"{main_link}page{iter}/")  # Отправляем запрос на текущую страницу
        print(f"{main_link}page{iter}/")  # Выводим ссылку на текущую страницу в консоль
        html = response.content  # Получаем содержимое страницы
        save_links(html)  # Сохраняем ссылки на все публикации, которые есть на странице
        iter += 1  # Увеличиваем итератор

# Сохраняем ссылки на публикации, с проверкой на валидность ссылки.
# Иногда попадаются ссылки от других авторов
def save_links(page_content):
    soup = BS(page_content, "html.parser")  # Создаем объект BeautifulSoup для парсинга HTML
    link_tag = soup.find_all('a', {'class': 'tm-title__link'})  # Находим все теги <a>, содержащие ссылки
    link_pattern = re.compile(r'/ru/companies/ru_mts/.*')  # Паттерн для валидации ссылки

    num_links = len(link_tag)  # Получаем количество найденных ссылок
    print(f"Number of links: {num_links}")  # Выводим количество ссылок в консоль

    for link_tags in link_tag:  # Итерируемся по найденным тегам <a>
        link = link_tags.get('href')  # Получаем ссылку из тега
        if link_pattern.match(link):  # Проверяем ссылку на валидность
            with open('links.txt', 'a') as f:  # Добавляем в файл, если ссылка валидна
                f.write(f"https://habr.com{link}\n")

if __name__ == '__main__':
    get_links() # Запускаем функцию, если нужно обновить файл с ссылками
    main()  # Запускаем основную функцию при выполнении скрипта
