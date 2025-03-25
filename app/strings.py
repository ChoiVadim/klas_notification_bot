from enum import Enum
from typing import Dict


class Language(Enum):
    EN = "English 🇬🇧"
    KO = "한국어 🇰🇷"
    RU = "Русский 🇷🇺"


class Strings:
    _strings: Dict[Language, Dict[str, str]] = {
        Language.EN: {
            "test_string": "Welcome, Test User!",
            "nonexistent_key": "Nonexistent key",
            "welcome": """Welcome, {name}! 👋
I'm a helpful bot for Kwangwoon University students 🏫
I track your assignments and send reminders for upcoming deadlines 🧭

Here's how to get started:
• /register - Set up your account
• /unregister - Delete your account 
• /language - Choose your preferred language
• /show - View all your upcoming tasks
• /search book_name - Find books in the library 🔍

You can also chat with me directly about university-related questions!
Find more helpful commands by tapping the menu button at the bottom left of your screen!

If something is not working or you have a problem, feel free to contact me @tsoivadim 💬
I'll help you out quickly!
""",
            "enter_username": "🎓 Please enter your student ID (I'll keep this secure)",
            "enter_password": "🔑 Please enter your KLAS password (this will be encrypted)",
            "enter_phone_number": "📱 Please enter your phone number",
            "library_enter_username": "🎓 Please enter your library account username",
            "library_enter_password": "🔑 Please enter your library account password",
            "invalid_credentials": "Hmm, those credentials don't seem to match our records. Please check your username and password, then try /register again 🔄",
            "library_login_failed": "We couldn't log you into the library with those details. Please verify your username, password and phone number, then try /lregister again 🔄",
            "registration_successful": "🎉 Registration complete! You'll now receive helpful notifications. Explore available features with /show or /info",
            "library_registration_successful": "🎉 Library access granted! You can now use the awesome library features, such as /qr",
            "registration_failed": "We couldn't complete your registration. Please check your details and try again with /register 🔄",
            "failed_to_save_credentials": "We had a small issue saving your credentials. Please try again later.",
            "unregistered": "You've successfully unregistered from the bot. You can always register again! 👋",
            "need_to_register": "This feature requires registration. Start with /register - it only takes a minute! ✨",
            "no_assignments": "🎉 Great news! You have no upcoming assignments",
            "failed_to_fetch_student_info": "We couldn't retrieve your student information right now. Let's try again later!",
            "unexpected_error": "Oops! We encountered a small issue. Please try again in a few moments! 🔄",
            "callback_error": "Please tap the buttons one at a time 😊",
            "donate_title": "Support this project with a coffee! ☕",
            "donate_description": "Your contribution helps keep this bot running and improving. Thank you for your support!",
            "choose_donation_amount": "Select an amount you'd like to contribute:",
            "successful_payment": "✅ Thank you for your generous support! Your contribution helps make this bot better for everyone.",
            "refund_error": "To request a refund, please reply directly to the payment message.",
            "refund_success": "✅ Your refund has been processed successfully. Thank you for your interest in supporting the bot.",
            "refund_error_message": "We couldn't process your refund right now. Please try again later.",
            "library_user_not_found": "You'll need to connect your library account first. Please use the /lregister command to get started.",
            "failed_to_fetch_news": "We couldn't load the latest news right now. Let's try again later.",
            "choose_news_type": "What type of news would you like to see?",
            "please_enter_book_name": "Please enter the name of the book you're looking for after the /search command.",
            "no_books_found": "I couldn't find any books matching that title. Double-check the spelling and try again! 📚",
            "todo_list_header": "📋 Here's what's on your schedule:\n\n\n",
            "time_left": "⏰ Time remaining: {time_str}",
            "lectures": "{count} lectures pending",
            "homeworks": "{count} assignments pending",
            "quizzes": "{count} quizzes pending",
            "team_projects": "{count} team projects pending",
            "too_many_messages": "I see you're sending messages quickly! Please pause briefly so I can catch up with your requests.",
            "student_info": """📚 Student Profile:
👨‍🎓 Name: {name} (ID: {uid})
Major: {major}
Year: {grade} | Semester: {semester}
🎯 Credits Summary:
• Total: {total_credits}
• Major: {major_credits_total}
• Elective: {elective_credits_total}
• GPA: {average_score} 📈""",
            "school_food_info": """
🍳 <Breakfast Special - 1000 KRW>
Available 8:30AM - 9:30AM at 복지관 2nd floor

🍔 <Lunch Options - 6000 KRW> 
Available 11:30AM - 2:00PM at 복지관 2nd floor

🍴 <Food Court Variety - 8000 KRW>
Available 11:30AM - 2:00PM at 연구관 B1 floor

All options are buffet-style! Pay once and enjoy as much as you like 🍴
""",
            "school_closed_on_weekend": "The university cafeterias are closed on weekends. Looking forward to serving you again on Monday! 🍽️",
            "foreigners_news": "🌏 International News",
            "all_news": "📰 All News",
            "tomorrow_menu": "🗓️ Tomorrow's Menu",
            "info": "ℹ️ More Info",
            "read_more": "📖 Read Full Article",
            "language_changed": "✅ Perfect! Your language preference has been updated.",
            "language_change_failed": "Please use /register first so I can save your language preference",
            "language_choice": "🌐 Choose your preferred language",
            "school_food_menu_header": "🍴 {day}'s Dining Options 🍴\n\n",
            "donate_title": "Buy me a coffee!😁",
            "donate_description": "Thank you for using my bot!",
            "choose_donation_amount": "Please choose a donation amount:",
            "successful_payment": "✅ Payment successful!",
            "refund_error": "Please reply to a payment message to request a refund!",
            "refund_success": "✅ Refund has been processed successfully.",
            "refund_error_message": "❌ Refund request was not successful. Please try again later.",
            "library_user_not_found": "🚫 You need to login to library first, please use /lregister command",
            "failed_to_fetch_news": "🚨 Failed to fetch news. Please try again later.",
            "choose_news_type": "Choose a type of news",
            "please_enter_book_name": "/search command requires a book name.",
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
            "school_food_menu_header": "🍴 {day}'s School Food Menu 🍴\n\n",
            "chat_about_university": "Feel free to ask me any questions about the university! I can help with information about campus facilities, academic policies, and more.",
        },


        
        Language.KO: {
            "test_string": "환영합니다!",
            "welcome": """안녕하세요, {name}님! 👋
광운대학교 학생들을 위한 도우미 봇입니다 🏫
과제를 추적하고 마감일 알림을 보내드려요 🧭

시작하는 방법:
• /register - 계정을 등록하세요
• /unregister - 계정을 삭제하세요
• /language - 원하는 언어를 선택하세요
• /show - 예정된 모든 과제를 확인하세요
• /search 책이름 - 도서관에서 책을 검색하세요 🔍

저와 직접 대화하면서 대학 관련 질문을 하실 수도 있어요!
더 많은 유용한 명령어는 화면 왼쪽 하단의 메뉴 버튼에서 확인하실 수 있어요

무언가 작동하지 않거나 문제가 있으시면 @tsoivadim 에게 연락주세요 💬
빠르게 도와드리겠습니다!""",
            "enter_username": "🎓 학번을 입력해주세요 (안전하게 보관됩니다)",
            "enter_password": "🔑 KLAS 비밀번호를 입력해주세요 (암호화됩니다)",
            "enter_phone_number": "📱 전화번호를 입력해주세요",
            "library_enter_username": "🎓 도서관 계정 사용자 이름을 입력해주세요",
            "library_enter_password": "🔑 도서관 계정 비밀번호를 입력해주세요",
            "invalid_credentials": "입력하신 정보가 기록과 일치하지 않네요. 사용자 이름과 비밀번호를 확인하고 /register 로 다시 시도해주세요 🔄",
            "library_login_failed": "입력하신 정보로 도서관 로그인을 할 수 없었어요. 사용자 이름, 비밀번호, 전화번호를 확인하고 /lregister 로 다시 시도해주세요 🔄",
            "registration_successful": "🎉 등록이 완료되었습니다! 이제 유용한 알림을 받을 수 있습니다. /show 또는 /info 명령어로 기능을 살펴보세요",
            "library_registration_successful": "🎉 도서관 접근 권한이 부여되었습니다! 이제 /qr과 같은 도서관 기능을 사용할 수 있습니다",
            "registration_failed": "등록을 완료할 수 없습니다. 세부 정보를 확인하고 /register로 다시 시도해 주세요 🔄",
            "failed_to_save_credentials": "자격 증명을 저장하는 데 작은 문제가 있었습니다. 나중에 다시 시도해 주세요.",
            "unregistered": "봇에서 성공적으로 등록이 취소되었습니다. 언제든지 다시 등록할 수 있습니다! 👋",
            "need_to_register": "이 기능을 사용하려면 등록이 필요합니다. /register로 시작하세요 - 단 1분이면 됩니다! ✨",
            "no_assignments": "🎉 좋은 소식! 예정된 과제가 없습니다",
            "failed_to_fetch_student_info": "지금은 학생 정보를 가져올 수 없습니다. 나중에 다시 시도해 주세요!",
            "unexpected_error": "이런! 작은 문제가 발생했습니다. 잠시 후 다시 시도해 주세요! 🔄",
            "callback_error": "버튼을 한 번에 하나씩만 눌러주세요 😊",
            "donate_title": "프로젝트를 커피 한 잔으로 응원해주세요! ☕",
            "donate_description": "여러분의 기부는 이 봇이 계속 운영되고 개선되는 데 도움이 됩니다. 지원해주셔서 감사합니다!",
            "choose_donation_amount": "기부하고 싶은 금액을 선택해주세요:",
            "successful_payment": "✅ 후원해주셔서 감사합니다! 여러분의 기여는 이 봇을 모두에게 더 좋게 만듭니다.",
            "refund_error": "환불을 요청하시려면 결제 메시지에 직접 답장해주세요.",
            "refund_success": "✅ 환불이 성공적으로 처리되었습니다. 봇 지원에 관심을 가져주셔서 감사합니다.",
            "refund_error_message": "지금은 환불을 처리할 수 없었어요. 나중에 다시 시도해주세요.",
            "library_user_not_found": "먼저 도서관 계정을 연결해야 합니다. /lregister 명령어로 시작해보세요.",
            "failed_to_fetch_news": "지금은 최신 뉴스를 불러올 수 없었어요. 나중에 다시 시도해보세요.",
            "choose_news_type": "어떤 종류의 뉴스를 보고 싶으신가요?",
            "please_enter_book_name": "찾으시는 책의 이름을 /search 명령어 뒤에 입력해주세요.",
            "no_books_found": "해당 제목의 책을 찾을 수 없었어요. 철자를 확인하고 다시 시도해보세요! 📚",
            "todo_list_header": "📋 여기 일정이 있습니다:\n\n\n",
            "time_left": "⏰ 남은 시간: {time_str}",
            "lectures": "강의 {count}개 예정",
            "homeworks": "과제 {count}개 예정",
            "quizzes": "퀴즈 {count}개 예정",
            "team_projects": "팀 프로젝트 {count}개 예정",
            "too_many_messages": "메시지를 빠르게 보내고 계시네요! 제가 요청을 처리할 수 있도록 잠시만 기다려주세요.",
            "chat_about_university": "대학교에 관한 어떤 질문이든 자유롭게 물어보세요! 캠퍼스 시설, 학사 정책 등에 대한 정보를 도와드릴 수 있어요.",
            "student_info": """📚 학생 프로필:
👨‍🎓 이름: {name} (학번: {uid})
전공: {major}
학년: {grade} | 학기: {semester}
🎯 학점 요약:
• 총 학점: {total_credits}
• 전공 학점: {major_credits_total}
• 교양 학점: {elective_credits_total}
• 평균 점수: {average_score} 📈""",
            "school_food_info": """
🍳 <아침 특가 - 1000원>
복지관 2층에서 오전 8:30 - 9:30에 이용 가능

🍔 <점심 옵션 - 6000원> 
복지관 2층에서 오전 11:30 - 오후 2:00에 이용 가능

🍴 <푸드코트 다양한 메뉴 - 8000원>
연구관 지하 1층에서 오전 11:30 - 오후 2:00에 이용 가능

모든 옵션은 뷔페 스타일! 한 번 결제하고 원하는 만큼 즐기세요 🍴
""",
            "school_closed_on_weekend": "대학 식당은 주말에 운영하지 않습니다. 월요일에 다시 뵙겠습니다! 🍽️",
            "foreigners_news": "🌏 국제 뉴스",
            "all_news": "📰 모든 뉴스",
            "tomorrow_menu": "🗓️ 내일 메뉴",
            "info": "ℹ️ 더 알아보기",
            "read_more": "📖 전체 기사 읽기",
            "language_changed": "✅ 완벽해요! 언어 설정이 업데이트되었습니다.",
            "language_change_failed": "언어 설정을 저장하려면 먼저 /register 를 사용해주세요",
            "language_choice": "🌐 원하는 언어를 선택하세요",
            "school_food_menu_header": "🍴 {day} 식사 옵션 🍴\n\n",
        },
        Language.RU: {
            "test_string": "Добро пожаловать!",
            "welcome": """Привет, {name}! 👋
Я бот-помощник для студентов университета Квангвун 🏫
Я отслеживаю задания и отправляю уведомления о сроках 🧭

Как начать:
• /register - зарегистрируйте свой аккаунт
• /unregister - удалите свой аккаунт
• /language - выберите удобный язык
• /show - просмотрите все предстоящие задания
• /search название_книги - найдите книгу в библиотеке 🔍

Вы также можете напрямую общаться со мной и задавать вопросы об университете!
Больше полезных команд доступно в меню в левом нижнем углу экрана!

Если что-то не работает или у вас есть проблемы, напишите мне @tsoivadim 💬
Я исправлю всё быстро!
""",
            "enter_username": "🎓 Введите ваш студенческий номер",
            "enter_password": "🔑 Введите ваш пароль от KLAS (будет зашифрован)",
            "enter_phone_number": "📱 Введите ваш номер телефона в формате 01012345678",
            "library_enter_username": "🎓 Введите ваш студенческий номер",
            "library_enter_password": "🔑 Введите пароль от библиотечного аккаунта (обычно ваш день рождения в формате 970326)",
            "invalid_credentials": "Данные не совпадают с данными Университета. Проверьте имя пользователя и пароль, затем попробуйте снова с /register 🔄",
            "library_login_failed": "Не удалось войти в библиотеку с указанными данными. Проверьте имя пользователя, пароль и номер телефона, затем попробуйте снова с /lregister 🔄",
            "registration_successful": "🎉 Регистрация завершена! Теперь вы будете получать полезные уведомления. Изучите доступные функции с помощью /show или /info",
            "library_registration_successful": "🎉 Доступ к библиотеке предоставлен! Теперь вы можете использовать замечательные библиотечные функции, такие как /qr",
            "registration_failed": "Не удалось завершить регистрацию. Проверьте данные и попробуйте снова с /register 🔄",
            "failed_to_save_credentials": "Возникла небольшая проблема при сохранении данных. Пожалуйста, попробуйте позже.",
            "unregistered": "Вы успешно отменили регистрацию в боте. Вы всегда можете зарегистрироваться снова! 👋",
            "need_to_register": "Для этой функции требуется регистрация. Начните с /register - это займет всего минуту! ✨",
            "no_assignments": "🎉 Отличные новости! У вас нет предстоящих заданий",
            "failed_to_fetch_student_info": "Не удалось получить информацию о студенте сейчас. Может, попробуем позже?",
            "unexpected_error": "Ой! Возникла небольшая проблема. Попробуйте еще раз через некоторое время! 🔄",
            "callback_error": "Пожалуйста, нажимайте кнопки по одной 😊",
            "donate_title": "Поддержите проект чашкой кофе! ☕",
            "donate_description": "Ваше пожертвование помогает поддерживать работу и улучшать этого бота. Спасибо за вашу поддержку!",
            "choose_donation_amount": "Выберите сумму, которую хотите пожертвовать:",
            "successful_payment": "✅ Спасибо за вашу поддержку! Ваш вклад помогает сделать этого бота лучше для всех.",
            "refund_error": "Для запроса возврата, пожалуйста, ответьте прямо на сообщение о платеже.",
            "refund_success": "✅ Возврат успешно обработан. Спасибо за интерес к поддержке бота.",
            "refund_error_message": "Не удалось обработать возврат сейчас. Пожалуйста, попробуйте позже.",
            "library_user_not_found": "Сначала вам нужно подключить библиотечный аккаунт. Начните с команды /lregister.",
            "failed_to_fetch_news": "Не удалось загрузить свежие новости сейчас. Попробуйте позже.",
            "choose_news_type": "Какой тип новостей вы хотели бы увидеть?",
            "please_enter_book_name": "Пожалуйста, введите название книги, которую вы ищете, после команды /search.",
            "no_books_found": "Не удалось найти книги с таким названием. Проверьте написание и попробуйте снова! 📚",
            "todo_list_header": "📋 Вот ваши задания:\n\n\n",
            "time_left": "⏰ Осталось времени: {time_str}",
            "lectures": "Предстоит {count} лекций",
            "homeworks": "Предстоит {count} домашних заданий",
            "quizzes": "Предстоит {count} тестов",
            "team_projects": "Предстоит {count} групповых проектов",
            "too_many_messages": "Вы отправляете сообщения слишком быстро! Пожалуйста, дайте мне немного времени обработать ваши запросы.",
            "chat_about_university": "Не стесняйтесь задавать мне любые вопросы об университете! Я могу помочь с информацией о кампусе, учебных правилах и многом другом.",
            "student_info": """📚 Профиль студента:
👨‍🎓 Имя: {name} (№: {uid})
Специальность: {major}
Курс: {grade} | Семестр: {semester}
🎯 Сводка по кредитам:
• Всего кредитов: {total_credits}
• Кредиты по специальности: {major_credits_total}
• Кредиты по выборным: {elective_credits_total}
• Средний балл: {average_score} 📈""",
            "school_food_info": """
🍳 <Завтрак - 1000 вон>
Доступно на 2-м этаже 복지관 с 8:30 до 9:30 утра

🍔 <Обед - 6000 вон> 
Доступно на 2-м этаже 복지관 с 11:30 до 14:00

🍴 <Обед (фудкорт) - 8000 вон>
Доступно в подвале 연구관 с 11:30 до 14:00

Все варианты в стиле шведского стола! Заплатите один раз и наслаждайтесь сколько хотите 🍴
""",
            "school_closed_on_weekend": "Университетская столовая не работает в выходные. Увидимся в понедельник! 🍽️",
            "foreigners_news": "🌏 Международные новости",
            "all_news": "📰 Все новости",
            "tomorrow_menu": "🗓️ Меню на завтра",
            "info": "ℹ️ Подробнее",
            "read_more": "📖 Читать полную статью",
            "language_changed": "✅ Отлично! Язык успешно обновлен.",
            "language_change_failed": "Чтобы сохранить настройки языка, сначала используйте /register",
            "language_choice": "🌐 Выберите предпочитаемый язык",
            "school_food_menu_header": "🍴 Варианты питания на {day} 🍴\n\n",
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
