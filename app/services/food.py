import aiohttp
import asyncio
import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.strings import Strings, Language


local_cache = {}


async def fetch_weekly_menu():
    url = "https://www.kw.ac.kr/ko/life/facility11.jsp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            beautiful_soup = BeautifulSoup(await response.text(), "html.parser")
            table_scroll_box = beautiful_soup.find("div", {"class": "table-scroll-box"})
            if table_scroll_box:
                menu_items = [
                    td.text.strip()
                    for td in table_scroll_box.find_all("td", {"class": "vt al"})
                ]
                # Store the menu for each day in the cache
                for i in range(len(menu_items)):
                    local_cache[i] = f"{menu_items[i]}"
            else:
                return False


def clear_cache_if_monday():
    # Clear the cache if today is Monday
    if datetime.now().weekday() == 0:
        local_cache.clear()


async def get_menu_for_day(day_index: int, user_lang: Language):
    clear_cache_if_monday()
    if user_lang == Language.RU:
        days_of_week = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
        ]
    elif user_lang == Language.KO:
        days_of_week = [
            "월요일",
            "화요일",
            "수요일",
            "목요일",
            "금요일",
        ]
    else:
        days_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]
    header = Strings.get(
        "school_food_menu_header", user_lang, day=days_of_week[day_index]
    )

    # Check if the cache is empty or doesn't have the current week's data
    if not local_cache or day_index not in local_cache:
        logging.info(f"Fetching weekly menu for {days_of_week[day_index]}")
        await fetch_weekly_menu()

    return header + local_cache.get(day_index, "🚨 No data found 🚨")


async def get_today_school_food_menu(user_lang: Language):
    today_index = datetime.now().weekday() % 7
    if today_index > 4:
        return Strings.get("school_closed_on_weekend", user_lang)
    return await get_menu_for_day(today_index, user_lang)


async def get_tomorrow_school_food_menu(user_lang: Language):
    tomorrow_index = (datetime.now().weekday() + 1) % 7
    if tomorrow_index > 4:
        return Strings.get("school_closed_on_weekend", user_lang)
    return await get_menu_for_day(tomorrow_index, user_lang)


async def get_school_food_info(user_lang: Language):
    return Strings.get("school_food_info", user_lang)


if __name__ == "__main__":
    print(asyncio.run(get_today_school_food_menu(Language.EN)))
    print(asyncio.run(get_tomorrow_school_food_menu(Language.EN)))
    print(local_cache)
