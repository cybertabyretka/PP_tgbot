from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MBTI_buttons = [
    [
        InlineKeyboardButton(text="ENTP (Полемист)", callback_data='entp'),
        InlineKeyboardButton(text="ISFP (Артист)", callback_data='isfp'),
        InlineKeyboardButton(text="ESFJ (Консул)", callback_data='esfj'),
        InlineKeyboardButton(text="INTJ (Стратег)", callback_data='intj')
    ],
    [
        InlineKeyboardButton(text="ENFJ (Тренер)", callback_data='enfj'),
        InlineKeyboardButton(text="ISTJ (Администратор)", callback_data='istj'),
        InlineKeyboardButton(text="INFP (Посредник)", callback_data='infp'),
        InlineKeyboardButton(text="ESTP (Делец)", callback_data='estp')
    ],
    [
        InlineKeyboardButton(text="INTP (Учёный)", callback_data='intp'),
        InlineKeyboardButton(text="ESFP (Развлекатель)", callback_data='esfp'),
        InlineKeyboardButton(text="ENTJ (Командир)", callback_data='entj'),
        InlineKeyboardButton(text="ISFJ (Защитник)", callback_data='isfj')
    ],
    [
        InlineKeyboardButton(text="ESTJ (Менеджер)", callback_data='estj'),
        InlineKeyboardButton(text="INFJ (Активист)", callback_data='infj'),
        InlineKeyboardButton(text="ENFP (Боец)", callback_data='enfp'),
        InlineKeyboardButton(text="ISTP (Виртуоз)", callback_data='istp')
    ]
]

MBTI_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=MBTI_buttons)

MMPI_buttons = [
    [
        InlineKeyboardButton(text="шизоидный", callback_data='sh'),
        InlineKeyboardButton(text="параноидальный", callback_data='pa'),
        InlineKeyboardButton(text="нарциссический", callback_data='na'),
        InlineKeyboardButton(text="психопатический", callback_data='ps')
    ],
    [
        InlineKeyboardButton(text="компульсивный", callback_data='ko'),
        InlineKeyboardButton(text="истерический", callback_data='is'),
        InlineKeyboardButton(text="депрессивный", callback_data='de'),
        InlineKeyboardButton(text="мазохистический", callback_data='ma')
    ]
]

MMPI_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=MMPI_buttons)
