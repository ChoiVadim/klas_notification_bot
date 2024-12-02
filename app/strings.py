from enum import Enum
from typing import Dict


class Language(Enum):
    EN = "en"
    KO = "ko"
    RU = "ru"


class Strings:
    _strings: Dict[Language, Dict[str, str]] = {
        Language.EN: {
            "welcome": """Welcome, {name}!
This bot is made for the students of Kwangwoon University 🏫
This bot will track your all assignments and notify you when they are less than 24 hours left 🧭

/register to start registration
/unregister to delete all your information from the bot
/show If you want to see all your tasks to do 🔍
/info If you want to see your graduation information 📝

❗ You need to register to use main features. This bot will encrypt your password and username. I do not save your credentials in visible form. So don't worry about your privacy.

I would appreciate if you could help me to improve this bot.
Send me any feedback or suggestions to @tsoivadim 💬
And i will try to improve this bot as soon as possible!

Made with ❤️ by @tsoivadim""",
            "enter_username": "🔄 Please enter your Kwangwoon University username:",
            "enter_password": "🔑 Please enter your password:",
            "invalid_credentials": "🚫 Invalid credentials. Please check your username and password and try again with /register",
            "registration_successful": "🎉 Registration successful! You will now receive notifications.",
            "registration_failed": "🚫 Registration failed. Please check your credentials and try again with /register",
            "failed_to_save_credentials": "🚨 Failed to save your credentials. Please try again later.",
            "unregistered": "🚫 You have been unregistered from the bot!",
            "need_to_register": "🚫 You need to register first. Use /register to start.",
            "no_assignments": "🚫 No assignments found or failed to fetch assignments.",
            "no_assignments": "Good job! You have no assignments to do right now 🎉",
            "failed_to_fetch_student_info": "🚨 Failed to fetch student information. Please try again later.",
            "unexpected_error": "🚨 Oops, something went wrong. Please try again later!",
            "library_user_not_found": "🚫 You need to login to library first, please use /lregister command",
            "student_info": """ UID: {uid} 
👨‍🎓 Name: {name} 
Major: {major}
Grade: {grade} Semester: {semester}
🎯 Total Credits: {total_credits}/{required_credits}
Major Credits: {major_credits_total}/{major_credits_required}
Elective Credits: {elective_credits_total}/{elective_credits_required}
Average Score: {average_score} 📈

❗ Recommendation: take at least {credits_per_semester} credits each semester and {major_credits_per_semester} major credits each semester to graduate on time!

P.S. As a foreigner student, we don't need to care about elective credits but if you have TOPIC less than 4, you need to take Korean language classes and get TOPIC 4 at least before graduation 🇰🇷""",
            "school_food_info": """
🍳 <1000KRW breakfast>
1000 KRW breakfast available from 8:30AM ~9:30AM at 복지관 2층

🍔 <Lunch> 
6000 KRW lunch available from 11:30 AM to 14:00 PM at 복지관 2층

🍴 <Food court>
8000 KRW meal available from 11:30 AM to 14:00 PM at 연구관 지하1층

Everything is a buffet, so you can pay once and eat as much as you want 🍴
""",
            "school_closed_on_weekend": "🚫 Cafeteria is closed on the weekend ",
        },
        Language.KO: {
            "welcome": """안녕하세요, {name}님!👋
이 봇은 광운대학교 학생들을 위해 만들어졌습니다 🏫
...""",
            # Add Korean translations
        },
        Language.RU: {
            "welcome": """Добро пожаловать, {name}!👋
Этот бот создан для студентов университета Квангвун 🏫
...""",
            # Add Russian translations
        },
    }

    @classmethod
    def get(cls, key: str, lang: Language = Language.EN, **kwargs) -> str:
        """Get string by key and language with optional formatting"""
        try:
            return cls._strings[lang][key].format(**kwargs)
        except KeyError:
            # Fallback to English if translation not found
            return cls._strings[Language.EN][key].format(**kwargs)
