import logging
import aiohttp
import asyncio
import time

from bs4 import BeautifulSoup

news_cache = []
last_fetch_time = 0


async def fetch_news():
    global last_fetch_time
    url = "https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=10"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
            table_scroll_box = beautiful_soup.find("div", {"class": "board-list-box"})
            if table_scroll_box:
                for item in table_scroll_box.find_all("li"):
                    link = "https://www.kw.ac.kr" + item.find("a").get("href")
                    title = (
                        item.find("a")
                        .text.replace("\n", "")
                        .replace("Attachment", "")
                        .replace("\r", " ")
                        .replace("  ", "")
                        .strip()
                    )
                    date = (
                        item.find("p", {"class": "info"})
                        .text.split("|")[2]
                        .replace("수정일", "")
                        .strip()
                    )
                    news_cache.append({"title": title, "link": link, "date": date})
    last_fetch_time = time.time()


async def get_news():
    global last_fetch_time
    if not news_cache or time.time() - last_fetch_time > 3600:
        logging.info("Fetching news from the website")
        await fetch_news()
    return news_cache


if __name__ == "__main__":
    from pprint import pprint

    pprint(asyncio.run(get_news()))
