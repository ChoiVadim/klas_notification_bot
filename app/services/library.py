import logging
import asyncio
import aiohttp
import ssl

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

    # Create a context that doesn't verify SSL
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, ssl=ssl_context) as response:
                beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
                table_scroll_box = beautiful_soup.find(
                    "ul", {"class": "resultList resultDetail"}
                )
                if table_scroll_box:
                    for item in table_scroll_box.find_all("li"):
                        title = item.find("dd", {"class": "title"}).find("a").text
                        image_link = item.find("dd", {"class": "book"}).find("img")[
                            "src"
                        ]

                        isInLibrary = item.find(
                            "div", {"class": "holding"}
                        ).text.strip()
                        print(isInLibrary)

                        if isInLibrary:
                            location = isInLibrary.find("td", class_="location").text
                            list_of_books.append((title, image_link, location))
                            
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching books: {e}")
            return []

    return list_of_books


async def search_book(query: str):
    list_of_books = await fetch_books(query)
    return list_of_books


if __name__ == "__main__":
    from pprint import pprint

    pprint(asyncio.run(fetch_books("skill for success")))
