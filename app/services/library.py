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
                        print(title, info)


def generate_qr_code(student_id: str):
    # Convert the timestamp to a similar format: "YYYYMMDDHHMMSS"
    today = datetime.now().strftime("%Y%m%d")
    seconds = datetime.now().strftime("%H%M%S%f")[:11]

    final_code = f"_KW 0{student_id}{today}{seconds}"

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(final_code)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")

    # Ensure the temp directory exists
    os.makedirs("temp", exist_ok=True)

    # Save to a temporary file
    filename = f"images/qr_{student_id}.png"
    img.save(filename)

    return filename


if __name__ == "__main__":
    from pprint import pprint

    # pprint(asyncio.run(fetch_books("skill for success")))
    print("_KW 020222035022024120106353981236")
    pprint(generate_qr_code("2022203502"))
