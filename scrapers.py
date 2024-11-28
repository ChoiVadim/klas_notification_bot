import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup


async def get_school_food_menu(day_index: int):
    url = "https://www.kw.ac.kr/ko/life/facility11.jsp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
            table_scroll_box = beautiful_soup.find("div", {"class": "table-scroll-box"})
            if table_scroll_box:
                days_of_week = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
                day_of_week = days_of_week[day_index]
                menu_items = [
                    td.text.strip()
                    for td in table_scroll_box.find_all("td", {"class": "vt al"})
                ]
                # Assuming the first item in the list corresponds to Monday and so on
                day_menu = menu_items[day_index]
                pretty_menu = f"🍴 {day_of_week}'s School Food Menu: 🍴\n\n{day_menu}"
                return pretty_menu
            else:
                return "🚨 No data found 🚨"


async def get_today_school_food_menu():
    today_index = datetime.now().weekday()
    if today_index > 4:
        return "🚨 School is closed on the weekend 🚨"
    return await get_school_food_menu(today_index)


if __name__ == "__main__":
    print(get_today_school_food_menu())
