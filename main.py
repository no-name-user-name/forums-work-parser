import time
import os

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import telebot

from zwork.db import DataBase
from zwork.chrome import start_driver

BOT_TOKEN = os.environ.get('BOTAPI')
cid = os.environ.get('CID')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')


def main():
    driver = start_driver(profile='main', is_headless=True)
    driver.get('https://zelenka.guru/forums/910/?node_id=910&order=post_date&direction=desc')

    driver.find_element(By.CLASS_NAME, 'discussionListItems')
    html = driver.page_source

    soup = bs4(html, features='html.parser')
    posts_block = soup.find('div', class_="latestThreads")
    posts = posts_block.find_all('div', class_='discussionListItem')

    db = DataBase()

    for post in posts:
        try:
            tags_list = []

            url = 'https://zelenka.guru/' + post.find('a', class_='listBlock')['href']
            title = post.find('h3', class_='title').text.strip()
            tags_block = post.find('span', class_='threadTitle--prefixGroup')
            data = post.find('span', class_='startDate').text.strip()

            try:
                tags = tags_block.find_all('span', class_='prefix')
                for tag in tags:
                    tags_list.append(tag.text.strip())
            except AttributeError:
                pass
            msg = f"<b>{title}</b>\n"\
                  f"<a href='{url}'>Открыть</a>\n"\
                  f"Tags: {' | '.join(tags_list)}\n"\
                  f"{data}"

            if db.is_new_url(url):
                bot.send_message(cid, msg)
                time.sleep(3)

        except AttributeError:
            continue


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print(f"[*] Error: {e}")
        finally:
            time.sleep(60)
