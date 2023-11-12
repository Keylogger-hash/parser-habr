import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg
import time
BASE_URL = 'https://habr.com'

    # HUB_URLS = [f'{BASE_URL}/ru/hubs/python/articles/',
#             f'{BASE_URL}/ru/hubs/javascript/articles/']


async def get_post_links(session, hub_url):
    async with session.get(hub_url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        links = []
        for a in soup.find_all('article', class_='tm-articles-list__item'):
            id = a['id']
            links.append(f"{BASE_URL}/ru/articles/{id}")
        return links


async def parse_post(session, post_url):
    async with session.get(post_url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        post_id =post_url.split('/')[-1]
        title = soup.find('h1', class_='tm-title_h1').text
        date = soup.find('span', class_='tm-article-datetime-published').time['title']
        author = soup.find('a', class_='tm-user-info__username').text
        text = soup.find('div', class_='tm-article-body').text
        author_url = f"{BASE_URL}/ru/users/{author}/"

        data = {
            'post_id': int(post_id),
            'title': title,
            'date': date,
            'url': post_url,
            'text': text,
            'author': author,
            'author_url': author_url
        }
        return data


async def save_to_db(post, hub_url, conn):
    # c = await conn.cursor()
    title = post['title']
    date = post['date']
    url = post['url']
    author = post['author']
    author_url = post['author_url']
    hub = hub_url
    text = post['text']
    post_id = post['post_id']
    await conn.execute(f"""INSERT INTO posts (title, date, url, author, 
                                           author_url, hub,text,post_id) 
                       VALUES ($1,$2,$3,$4,$5,$6,$7,$8)""",title,date,url,author,author_url,hub,text,post_id)


async def check_post_exist(conn, url):
    row = await conn.fetchrow('SELECT * FROM posts WHERE url=$1',url)
    if row is None:
        return True
    return False

async def get_hubs(conn):
    rows = await conn.fetch("SELECT hub FROM hubs")
    return [row['hub'] for row in rows]

dsn = "postgres://user:password@db:5432/habr"
async def main():
    async with asyncpg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS hubs(id serial,hub text,delay int);''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS posts 
                                          (id SERIAL PRIMARY KEY, text text,title text, date text, url text, 
                                           author text, author_url text, hub text,post_id integer);''')
            while True:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
                    tasks = []
                    HUB_URLS = await get_hubs(conn)
                    for hub_url in HUB_URLS:
                        tasks.append(get_post_links(session, hub_url))
                    links_from_hubs = await asyncio.gather(*tasks)
                    for hub_url, links in zip(HUB_URLS, links_from_hubs):
                        tasks = []
                        for link in links:
                            is_exist = await check_post_exist(conn,link)
                            if not is_exist:
                                tasks.append(parse_post(session, link))
                        posts = await asyncio.gather(*tasks)

                        for post in posts:
                            await save_to_db(post, hub_url, conn)
                print("Reading is done")
                    # await conn.close()
                await asyncio.sleep(600)


asyncio.run(main())
