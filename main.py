import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://habr.com'
HUB_URL = f'{BASE_URL}/ru/hubs/python/articles/'


def get_post_links(hub_url):
    response = requests.get(hub_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a in soup.find_all('article', class_='tm-articles-list__item'):
        # print(a)
        id = a['id']
        links.append(f"{BASE_URL}/ru/articles/{id}")
    return links


def parse_post(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='tm-title_h1').text
    date = soup.find('span', class_='tm-article-datetime-published').text
    author = soup.find('a', class_='tm-user-info__username').text
    author_url = f"{BASE_URL}/ru/users/{author}/"

    data = {
        'title': title,
        'date': date,
        'url': post_url,
        'author': author,
        'author_url': author_url
    }
    return data


def main():
    while True:
        links = get_post_links(HUB_URL)
        print(links)
        for link in links:
            post = parse_post(link)
            print(post)

        time.sleep(600)
        print("Time sleep")


if __name__ == '__main__':
    main()

# Написать парсер любого хаба с habr.com на выбор. Условия:
# 1) Раз в 10 минут делать запрос на главную страницу хаба.
# 2) Взять с главной страницы хаба ссылки на статьи.
# 3) Для каждой собранной ссылки посетить страницу статьи и собрать информацию о статье (заголовок, дата, ссылка на пост, имя автор, ссылка на автора).
# 4) Вывести информацию на консоль.
# Опциональные усложнения:
# LVL1: Сохранять данные в базу данных PostgreSQL/sqlite3 с текстом публикации (повторяющиеся по ссылкам не сохранять).
# LVL2: Создать таблицу в базе данных с информацией о хабах.
#       Добавить в созданную таблицу 2-3 хаба.
#       Обходить все хабы из таблицы, а не только один изначально выбранный.
#       Сохранять для публикаций также хаб, с которого была взята публикация.
# LVL3: Сделать парсер асинхронным, используя библиотеку aiohttp, например, 5 параллельных запросов.
# LVL4: Добавить админку на Django для отображения хабов и управления ими (добавить хаб/удалить хаб/указать период обхода хаба).
# LVL5: Упаковать всё в Docker образ.