import os
from telebot import TeleBot, types

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))
user_language = {}

# Til tanlash klaviaturasi
def language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

# O‘zbekcha menyu
def main_menu_uz():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🤖 Bot haqida", "🛠 Xizmatlar")
    markup.add("🎓 Arab tili", "💎 Premium obuna")
    markup.add("🧪 Test bo‘limi")
    return markup

# Ruscha menyu
def main_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🤖 О боте", "🛠 Услуги")
    markup.add("🎓 Арабский язык", "💎 Премиум подписка")
    markup.add("🧪 Тестовый раздел")
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    user_language[message.chat.id] = None
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский"])
def choose_language(message):
    if message.text == "🇺🇿 O‘zbekcha":
        user_language[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Arabic Tester botiga xush kelibsiz!", reply_markup=main_menu_uz())
    else:
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Добро пожаловать в бот Arabic Tester!", reply_markup=main_menu_ru())

# O‘zbekcha bo‘limlar
def uzbek_sections(message):
    if message.text == "🤖 Bot haqida":
        text = (
            "Bu bot Arab tili bo‘yicha test va o‘quv xizmatlarini taqdim etadi.\n"
            "Darajalar, testlar va foydali manbalarni shu yerda topasiz."
        )
    elif message.text == "🛠 Xizmatlar":
        text = (
            "Quyidagi xizmatlar mavjud:\n"
            "- Arab tili bo‘yicha testlar\n"
            "- Daraja asosidagi materiallar\n"
            "- Online tarjimon"
        )
    elif message.text == "🎓 Arab tili":
        text = (
            "🎓 *Arab tili o‘quv tizimi:*\n"
            "- A1-A2, B1-B2, C1-C2 darajalar\n"
            "- Online testlar\n"
            "- Kitoblar va lug‘at bo‘limi\n"
            "- Tarjimon xizmatlari"
        )
    elif message.text == "💎 Premium obuna":
        text = (
            "💎 *Premium imkoniyatlari:*\n"
            "- Maxsus testlarga kirish\n"
            "- Statistikani ko‘rish\n"
            "- Qo‘shimcha bo‘limlar"
        )
    elif message.text == "🧪 Test bo‘limi":
        text = (
            "🧪 Testlar bo‘limi:\n"
            "- Boshlang‘ich (A1-A2)\n"
            "- O‘rta (B1-B2)\n"
            "- Yuqori (C1-C2)"
        )
    else:
        text = "Noto‘g‘ri buyruq. Menyudan tanlang yoki /help ni yozing."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Ruscha bo‘limlar
def russian_sections(message):
    if message.text == "🤖 О боте":
        text = (
            "Этот бот предоставляет тесты и учебные ресурсы по арабскому языку.\n"
            "Уровни, тесты и словари доступны здесь."
        )
    elif message.text == "🛠 Услуги":
        text = (
            "Доступные услуги:\n"
            "- Тесты по арабскому языку\n"
            "- Учебные материалы\n"
            "- Онлайн переводчик"
        )
    elif message.text == "🎓 Арабский язык":
        text = (
            "🎓 *Система изучения арабского языка:*\n"
            "- Уровни A1-A2, B1-B2, C1-C2\n"
            "- Онлайн тесты\n"
            "- Книги и словарь\n"
            "- Переводчик"
        )
    elif message.text == "💎 Премиум подписка":
        text = (
            "💎 *Премиум функции:*\n"
            "- Доступ к спец. тестам\n"
            "- Просмотр статистики\n"
            "- Новые разделы"
        )
    elif message.text == "🧪 Тестовый раздел":
        text = (
            "🧪 Раздел тестов:\n"
            "- Начальный (A1-A2)\n"
            "- Средний (B1-B2)\n"
            "- Продвинутый (C1-C2)"
        )
    else:
        text = "Команда не распознана. Введите /help или выберите из меню."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def help_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        help_text = (
            "Yordam buyruqlari:\n"
            "/start - Botni ishga tushurish\n"
            "/help - Yordamni ko‘rsatish\n"
            "/about - Bot haqida"
        )
    elif lang == "ru":
        help_text = (
            "Команды помощи:\n"
            "/start - Запустить бота\n"
            "/help - Помощь\n"
            "/about - О боте"
        )
    else:
        help_text = "Iltimos, tilni tanlang / Пожалуйста, выберите язык."
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, "Arabic Tester bot — arab tili bo‘yicha testlar va o‘quv xizmatlari uchun platforma.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        uzbek_sections(message)
    elif lang == "ru":
        russian_sections(message)
    else:
        bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())

bot.infinity_polling()
