import logging
import asyncio
import aiohttp
from io import BytesIO
from datetime import datetime
import os

import qrcode
from bs4 import BeautifulSoup


async def fetch_books(query: str):
    params = {
        "st": "KWRD",
        "si": "TOTAL",
        "x": "0",
        "y": "0",
        "q": query,
    }
    url = "https://kupis.kw.ac.kr/eds/brief/integrationResult"

    list_of_books = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
            table_scroll_box = beautiful_soup.find(
                "ul", {"class": "resultList resultDetail"}
            )
            if table_scroll_box:
                for item in table_scroll_box.find_all("li"):
                    title = item.find("dd", {"class": "title"}).find("a").text
                    isInLibrary = item.find("div", {"class": "holding"}).text.strip()
                    if isInLibrary:
                        info = item.find_all("dd", {"class": "info"})[2].text
                        list_of_books.append((title, info))

    return list_of_books


async def search_book(query: str):
    list_of_books = await fetch_books(query)
    return list_of_books


if __name__ == "__main__":
    from pprint import pprint

    pprint(asyncio.run(fetch_books("skill for success")))
