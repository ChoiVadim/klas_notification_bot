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
This bot will track your all assignments and notify you when they are less than 24 hours left, so you will not miss any important tasks🧭

/register to start registration
/language to change language
/show If you want to see all your tasks to do 
/search book_name If you want to search for a book in the library 🔍

You can see other commands clicking on the menu button below on the left side of the screen

❗ You need to register to use main features. This bot will encrypt your password and username.
I do not save your credentials in visible form. So don't worry about your privacy.

I would appreciate if you could help me to improve this bot.
Send me any feedback or suggestions to @tsoivadim 💬
And i will try to improve this bot as soon as possible!

Made with ❤️ by @tsoivadim""",
            "enter_username": "🎓 Please enter your student ID",
            "enter_password": "🔑 Please enter your KLAS password",
            "enter_phone_number": "📱 Please enter your phone number",
            "library_enter_username": "🎓 Please enter your library account username",
            "library_enter_password": "🔑 Please enter your library account password",
            "invalid_credentials": "🚫 Invalid credentials. Please check your username and password and try again with /register",
            "library_login_failed": "🚫 Login failed. Please check your username, password and phone number and try again with /lregister",
            "registration_successful": "🎉 Registration successful! You will now receive notifications. And you can use /show and /info commands",
            "library_registration_successful": "🎉 Library registration successful! Now you can use library features like /qr",
            "registration_failed": "🚫 Registration failed. Please check your credentials and try again with /register",
            "failed_to_save_credentials": "🚨 Failed to save your credentials. Please try again later.",
            "unregistered": "🚫 You have been unregistered from the bot!",
            "need_to_register": "🚫 You need to register first. Use /register to start.",
            "no_assignments": "🚫 No assignments found or failed to fetch assignments.",
            "no_assignments": "Good job! You have no assignments to do right now 🎉",
            "failed_to_fetch_student_info": "🚨 Failed to fetch student information. Please try again later.",
            "unexpected_error": "🚨 Oops, something went wrong. Please try again later!",
            "callback_error": "Please dont spam me!",
            "donate_title": "Buy me a coffee!😁",
            "donate_description": "Thank you for using my bot!",
            "successful_payment": "✅ Payment successful!",
            "refund_error": "Please reply to a payment message to request a refund!",
            "refund_success": "✅ Refund has been processed successfully.",
            "refund_error_message": "❌ Refund request was not successful. Please try again later.",
            "library_user_not_found": "🚫 You need to login to library first, please use /lregister command",
            "failed_to_fetch_news": "🚨 Failed to fetch news. Please try again later.",
            "choose_news_type": "Choose a type of news",
            "please_enter_book_name": "Please enter a book name after /search command.",
            "no_books_found": "🤔 No books found. Check your spelling and try again!",
            "todo_list_header": "📋 Your Todo List:\n\n\n",
            "time_left": "⏰ Time left: {time_str}",
            "lectures": "Lectures left: {count}",
            "homeworks": "Homeworks left: {count}",
            "quizzes": "Quizzes left: {count}",
            "team_projects": "Team projects left: {count}",
            "too_many_messages": "You are sending messages too quickly. Please wait a moment.",
            "student_info": """ UID: {uid} 
👨‍🎓 Name: {name} 
Major: {major}
Grade: {grade} Semester: {semester}
🎯 Total Credits: {total_credits}
Major Credits: {major_credits_total}
Elective Credits: {elective_credits_total}
Average Score: {average_score} 📈""",
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
            "foreigners_news": "🌏 Foreigners",
            "all_news": "📰 All",
            "tomorrow_menu": "🗓️ Tomorrow's Menu",
            "info": "ℹ️ Info",
            "read_more": "📖 Read more",
            "language_changed": "✅ Language changed successfully!",
            "language_change_failed": "❌ Please /register before changing language!",
            "language_choice": "🌐 Choose your language",
        },
        Language.KO: {
            "welcome": """안녕하세요, {name}님!👋
이 봇은 광운대학교 학생들을 위해 만들어졌습니다 🏫
이 봇은 모든 과제를 추적하고 24시간 이내에 남은 과제가 있을 때 알림을 보내드립니다. 중요한 과제를 놓치지 않도록 도와드립니다 🧭

/register 를 통해 등록을 시작하세요
/language 언어를 변경하세요
/show 모든 할 일 목록을 보고 싶다면
/search book_name 도서관에서 책을 검색하고 싶다면 🔍

화면 왼쪽 하단의 메뉴 버튼을 클릭하면 다른 명령어들을 볼 수 있습니다

❗ 주요 기능을 사용하려면 등록이 필요합니다. 이 봇은 비밀번호와 사용자 이름을 암호화합니다.
개인정보는 보이는 형태로 저장하지 않으니 안심하세요.

이 봇을 개선하는데 도움을 주시면 감사하겠습니다.
피드백이나 제안사항이 있으시다면 @tsoivadim 으로 보내주세요 💬
최대한 빨리 개선하도록 하겠습니다!

@tsoivadim 이 ❤️으로 만들었습니다""",
            "enter_username": "🎓 학번을 입력해주세요",
            "enter_password": "🔑 KLAS 비밀번호를 입력해주세요",
            "enter_phone_number": "📱 전화번호를 입력해주세요",
            "library_enter_username": "🎓 도서관 계정 사용자 이름을 입력해주세요",
            "library_enter_password": "🔑 도서관 계정 비밀번호를 입력해주세요",
            "invalid_credentials": "🚫 잘못된 인증정보입니다. 사용자 이름과 비밀번호를 확인하고 /register 명령어로 다시 시도해주세요",
            "library_login_failed": "🚫 로그인 실패. 사용자 이름, 비밀번호, 전화번호를 확인하고 /lregister 명령어로 다시 시도해주세요",
            "registration_successful": "🎉 등록 성공! 이제 알림을 받으실 수 있습니다. /show 와 /info 명령어를 사용하실 수 있습니다",
            "library_registration_successful": "🎉 도서관 등록 성공! 이제 /qr 과 같은 도서관 기능을 사용하실 수 있습니다",
            "registration_failed": "🚫 등록 실패. 인증정보를 확인하고 /register 명령어로 다시 시도해주세요",
            "failed_to_save_credentials": "🚨 인증정보 저장 실패. 나중에 다시 시도해주세요.",
            "unregistered": "🚫 봇 등록이 해제되었습니다!",
            "need_to_register": "🚫 먼저 등록이 필요합니다. /register 명령어로 시작하세요.",
            "no_assignments": "🎉 잘하셨습니다! 현재 할 과제가 없습니다",
            "failed_to_fetch_student_info": "🚨 학생 정보를 가져오는데 실패했습니다. 나중에 다시 시도해주세요.",
            "unexpected_error": "🚨 죄송합니다, 문제가 발생했습니다. 나중에 다시 시도해주세요!",
            "callback_error": "스팸을 보내지 말아주세요!",
            "donate_title": "커피 한 잔 사주세요!😁",
            "donate_description": "봇을 이용해주셔서 감사합니다!",
            "refund_error": "환불을 요청하려면 결제 메시지에 답장해주세요!",
            "successful_payment": "✅ 결제가 성공적으로 처리되었습니다.",
            "refund_success": "✅ 환불이 성공적으로 처리되었습니다.",
            "refund_error_message": "❌ 환불 요청이 실패했습니다. 나중에 다시 시도해주세요.",
            "library_user_not_found": "🚫 먼저 도서관 로그인이 필요합니다, /lregister 명령어를 사용해주세요",
            "failed_to_fetch_news": "🚨 뉴스를 가져오는데 실패했습니다. 나중에 다시 시도해주세요.",
            "choose_news_type": "뉴스 종류를 선택하세요",
            "please_enter_book_name": "/search 명령어 뒤에 책 이름을 입력해주세요.",
            "no_books_found": "🤔 책을 찾을 수 없습니다. 철자를 확인하고 다시 시도해주세요!",
            "todo_list_header": "📋 할 일 목록:\n\n\n",
            "time_left": "⏰ 남은 시간: {time_str}",
            "lectures": "강의 {count}개가 남았습니다",
            "homeworks": "과제 {count}개가 남았습니다",
            "quizzes": "퀴즈 {count}개가 남았습니다",
            "team_projects": "팀 프로젝트 {count}개가 남았습니다",
            "too_many_messages": "너무 빠르게 메시지를 보내고 있습니다. 잠시 기다려주세요.",
            "student_info": """학번: {uid} 
            
👨‍🎓 이름: {name} 
전공: {major}
학년: {grade} 학기: {semester}
🎯 총 학점: {total_credits}
전공 학점: {major_credits_total}
교양 학점: {elective_credits_total}
평균 점수: {average_score} 📈""",
            "school_food_info": """
🍳 <1000원 아침>
복지관 2층에서 오전 8:30 ~ 9:30에 1000원 아침식사 이용 가능

🍔 <점심> 
복지관 2층에서 오전 11:30 ~ 오후 2:00에 6000원 점심식사 이용 가능

🍴 <푸드코트>
연구관 지하1층에서 오전 11:30 ~ 오후 2:00에 8000원 식사 이용 가능

모든 메뉴는 뷔페식으로, 한 번 결제하면 원하는 만큼 드실 수 있습니다 🍴
""",
            "school_closed_on_weekend": "🚫 주말에는 식당이 운영하지 않습니다",
            "foreigners_news": "🌏 국제",
            "all_news": "📰 전체",
            "tomorrow_menu": "🍽️ 내일 식단",
            "info": "ℹ️ 정보",
            "read_more": "👀 자세히 보기",
            "language_changed": "✅ 언어가 성공적으로 변경되었습니다!",
            "language_change_failed": "❌ 언어 변경 실패. 먼저 /register 명령어를 사용해주세요",
        },
        Language.RU: {
            "welcome": """Добро пожаловать, {name}!
Этот бот создан для студентов университета Квангвун 🏫
Бот будет отслеживать все ваши задания и уведомлять вас, когда до сдачи останется менее 24 часов, чтобы вы не пропустили важные задачи 🧭

/register для начала регистрации
/language для изменения языка
/show Если хотите увидеть все ваши задания
/search название_книги Если хотите найти книгу в библиотеке 🔍

Другие команды можно увидеть, нажав на кнопку меню внизу слева экрана

❗ Для использования основных функций необходимо зарегистрироваться. Бот зашифрует ваш пароль и имя пользователя.
Я не сохраняю ваши учетные данные в видимой форме. Не беспокойтесь о своей конфиденциальности.

Буду признателен, если вы поможете улучшить этого бота.
Отправляйте любые отзывы или предложения на @tsoivadim 💬
И я постараюсь улучшить бота как можно скорее!

Сделано с ❤️ от @tsoivadim""",
            "enter_username": "🎓 Пожалуйста, введите ваш студенческий ID",
            "enter_password": "🔑 Пожалуйста, введите ваш пароль KLAS",
            "enter_phone_number": "📱 Пожалуйста, введите ваш номер телефона",
            "library_enter_username": "🎓 Пожалуйста, введите имя пользователя библиотечного аккаунта",
            "library_enter_password": "🔑 Пожалуйста, введите пароль библиотечного аккаунта",
            "invalid_credentials": "🚫 Неверные учетные данные. Проверьте имя пользователя и пароль и попробуйте снова с /register",
            "library_login_failed": "🚫 Ошибка входа. Проверьте имя пользователя, пароль и номер телефона и попробуйте снова с /lregister",
            "registration_successful": "🎉 Регистрация успешна! Теперь вы будете получать уведомления. И можете использовать команды /show и /info",
            "library_registration_successful": "🎉 Регистрация в библиотеке успешна! Теперь вы можете использовать библиотечные функции, такие как /qr",
            "registration_failed": "🚫 Регистрация не удалась. Проверьте ваши учетные данные и попробуйте снова с /register",
            "failed_to_save_credentials": "🚨 Не удалось сохранить ваши учетные данные. Попробуйте позже.",
            "unregistered": "🚫 Вы отменили регистрацию в боте!",
            "need_to_register": "🚫 Сначала нужно зарегистрироваться. Используйте /register для начала.",
            "no_assignments": "🎉 Отлично! У вас сейчас нет заданий",
            "failed_to_fetch_student_info": "🚨 Не удалось получить информацию о студенте. Попробуйте позже.",
            "unexpected_error": "🚨 Упс, что-то пошло не так. Попробуйте позже!",
            "callback_error": "Пожалуйста, не спамьте!",
            "donate_title": "Угостите меня кофе!😁",
            "donate_description": "Спасибо за использование моего бота!",
            "refund_error": "Пожалуйста, ответьте на сообщение об оплате, чтобы запросить возврат!",
            "successful_payment": "✅ Оплата прошла успешно!",
            "refund_success": "✅ Возврат успешно обработан.",
            "refund_error_message": "❌ Запрос на возврат не был успешным. Попробуйте позже.",
            "library_user_not_found": "🚫 Сначала нужно войти в библиотеку, используйте команду /lregister",
            "failed_to_fetch_news": "🚨 Не удалось получить новости. Попробуйте позже.",
            "choose_news_type": "Выберите тип новостей",
            "please_enter_book_name": "Пожалуйста, введите название книги после команды /search.",
            "no_books_found": "🤔 Книги не найдены. Проверьте правописание и попробуйте снова!",
            "todo_list_header": "📋 Ваш список дел:\n\n\n",
            "time_left": "⏰ Время до сдачи: {time_str}",
            "lectures": "Осталось лекций: {count}",
            "homeworks": "Осталось домашних заданий: {count}",
            "quizzes": "Осталось квизов: {count}",
            "team_projects": "Осталось командных заданий: {count}",
            "too_many_messages": "Вы отправляете сообщения слишком быстро. Пожалуйста, подождите немного.",
            "student_info": """ID: {uid} 
👨‍🎓 Имя: {name} 
Специальность: {major}
Курс: {grade} Семестр: {semester}
🎯 Всего кредитов: {total_credits}
Кредиты по специальности: {major_credits_total}
Факультативные кредиты: {elective_credits_total}
Средний балл: {average_score} 📈""",
            "school_food_info": """
🍳 <Завтрак за 1000 вон>
Завтрак за 1000 вон доступен с 8:30 до 9:30 на 2 этаже общежития

🍔 <Обед> 
Обед за 6000 вон доступен с 11:30 до 14:00 на 2 этаже общежития

🍴 <Фуд-корт>
Еда за 8000 вон доступна с 11:30 до 14:00 на B1 этаже исследовательского корпуса

Все работает по системе шведского стола, так что вы можете заплатить один раз и есть сколько хотите 🍴
""",
            "school_closed_on_weekend": "🚫 Столовая закрыта в выходные",
            "foreigners_news": "🌏 Иностранцы",
            "all_news": "📰 Все",
            "tomorrow_menu": "🍽️ Меню на завтра",
            "info": "ℹ️ Информация",
            "read_more": "📖 Читать далее",
            "language_changed": "✅ Язык успешно изменен!",
            "language_change_failed": "❌ Зарегистрируйтесь /register перед изменением языка",
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
