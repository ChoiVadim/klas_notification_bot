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
    thumbnail_url = "https://kupis.kw.ac.kr/openapi/thumbnail"
    base_url = "https://kupis.kw.ac.kr"
    list_of_books = []

    # Create a context that doesn't verify SSL
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, ssl=ssl_context) as response:
            if response.status == 200:
                beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
                table_scroll_box = beautiful_soup.find(
                    "ul", {"class": "resultList resultDetail"}
                )
                if table_scroll_box:
                    books = table_scroll_box.find_all("li")
                    if len(books) > 4:
                        books = books[:4]
                    else:
                        books = books[: len(books)]

                    for item in books:
                        title_elem = item.find("dd", {"class": "title"})
                        image_elem = item.find("dd", {"class": "book"})
                        holding_elem = item.find(
                            "div", {"class": "holding"}
                        ).text.strip()
                        location = ""
                        status = "Available"
                        return_date = "X"

                        if holding_elem:
                            title = title_elem.find("a").text.strip()
                            detail_url = base_url + title_elem.find("a")["href"]

                            # Extract book ID
                            book_id = image_elem.find("img")["id"].replace(
                                "bookImg_CATTOT", ""
                            )

                            # Get ISBN from detail page
                            async with session.get(
                                detail_url, ssl=ssl_context
                            ) as detail_response:
                                if detail_response.status == 200:
                                    detail_soup = BeautifulSoup(
                                        await detail_response.text(), "html.parser"
                                    )
                                    table_elem = (
                                        detail_soup.find(
                                            "table", {"class": "profiletable"}
                                        )
                                        .find("tbody")
                                        .find_all("tr")
                                    )

                                    isbn = ""
                                    for elem in table_elem:
                                        if elem.find("th").text.strip() == "ISBN":
                                            isbn = elem.find("td").text.strip()
                                            break

                                    final_isbn = ""
                                    for i in isbn:
                                        if i.isdigit():
                                            final_isbn += i

                                    location = detail_soup.find("td", class_="location")
                                    status = detail_soup.find(
                                        "span", class_="status ing"
                                    )
                                    return_date = detail_soup.find(
                                        "td", class_="returnDate"
                                    )

                                    if location:
                                        location = location.text.strip()
                                    if status:
                                        status = status.text.strip()
                                    if return_date:
                                        return_date = return_date.text.strip()

                                    # Get thumbnail
                                    thumbnail_data = {
                                        "isbn": final_isbn,
                                        "sysdiv": "CAT",
                                        "ctrl": book_id,
                                    }
                                    async with session.post(
                                        thumbnail_url,
                                        data=thumbnail_data,
                                        ssl=ssl_context,
                                    ) as thumb_response:
                                        if thumb_response.status == 200:
                                            image_data = await thumb_response.json()
                                            image_url = image_data.get(
                                                "largeUrl",
                                                image_data.get("smallUrl", None),
                                            )

                                    list_of_books.append(
                                        (
                                            title,
                                            image_url,
                                            location,
                                            status,
                                            return_date,
                                        )
                                    )
            else:
                logging.error(f"Failed to fetch books: {response.status}")
                return []

    return list_of_books


async def search_book(query: str):
    list_of_books = await fetch_books(query)
    return list_of_books


if __name__ == "__main__":
    from pprint import pprint
    import logging

    logging.basicConfig(level=logging.DEBUG)

    pprint(asyncio.run(fetch_books("시사한국어")))
