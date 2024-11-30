import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup

local_cache = {}


async def fetch_weekly_menu():
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
                ]
                menu_items = [
                    td.text.strip()
                    for td in table_scroll_box.find_all("td", {"class": "vt al"})
                ]
                # Store the menu for each day in the cache
                for i, day in enumerate(days_of_week):
                    local_cache[day] = (
                        f"🍴 {day}'s School Food Menu: 🍴\n\n{menu_items[i]}"
                    )
            else:
                for day in days_of_week:
                    local_cache[day] = "🚨 No data found 🚨"


def clear_cache_if_monday():
    # Clear the cache if today is Monday
    if datetime.now().weekday() == 0:
        local_cache.clear()


async def get_menu_for_day(day_index: int):
    clear_cache_if_monday()
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]
    day_of_week = days_of_week[day_index]

    # Check if the cache is empty or doesn't have the current week's data
    if not local_cache or day_of_week not in local_cache:
        await fetch_weekly_menu()

    return local_cache.get(day_of_week, "🚨 No data found 🚨")


async def get_today_school_food_menu():
    today_index = datetime.now().weekday() % 7
    if today_index > 4:
        return "🚨 School is closed on the weekend 🚨"
    return await get_menu_for_day(today_index)


async def get_tomorrow_school_food_menu():
    tomorrow_index = (datetime.now().weekday() + 1) % 7
    if tomorrow_index > 4:
        return "🚨 School is closed on the weekend 🚨"
    return await get_menu_for_day(tomorrow_index)


async def get_school_food_info():
    return """
<천원의 아침> is a meal that costs 1000 won and availabel only from 8.00 AM to 9.00 AM.
Location: 복지관 2층

<중식> is a meal that costs 3000 won and available from 11.00 AM to 1.00 PM.
Location: 복지관 2층

<푸드코트> is a meal that costs 4000 won and available from 11.00 AM to 1.00 PM.
Location: 복지관 1층
"""


if __name__ == "__main__":
    print(asyncio.run(get_today_school_food_menu()))
    print(asyncio.run(get_tomorrow_school_food_menu()))
    print(local_cache)
