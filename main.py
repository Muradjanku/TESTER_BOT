import os
from telebot import TeleBot, types

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))

user_language = {}

# Til tanlash klaviaturasi
def language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

# O‘zbekcha asosiy menyu (yangilangan)
def main_menu_uz():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Testlar", "Lug‘atlar")
    markup.add("Kitoblar", "Premium obuna")
    markup.add("Online 24/7")
    markup.add("938839873")
    return markup

# Ruscha asosiy menyu (yangilangan)
def main_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Тесты", "Словари")
    markup.add("Книги", "Премиум подписка")
    markup.add("Онлайн 24/7")
    markup.add("938839873")
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    user_language[message.chat.id] = None
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский"])
def choose_language(message):
    if message.text == "🇺🇿 O‘zbekcha":
        user_language[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Botga xush kelibsiz! Kerakli bo‘limni tanlang:", reply_markup=main_menu_uz())
    else:
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Добро пожаловать в бот! Выберите раздел:", reply_markup=main_menu_ru())

def uzbek_sections(message):
    if message.text == "Testlar":
        bot.send_message(message.chat.id, "Testlar bo‘limiga xush kelibsiz. Testlar tez orada qo‘shiladi.")
    elif message.text == "Lug‘atlar":
        bot.send_message(message.chat.id, "Lug‘atlar bo‘limi: Sizga kerakli lug‘atlarni shu yerda topishingiz mumkin.")
    elif message.text == "Kitoblar":
        bot.send_message(message.chat.id, "Kitoblar bo‘limi: O‘quv kitoblari ro‘yxati va yuklab olish havolalari.")
    elif message.text == "Premium obuna":
        bot.send_message(message.chat.id, "Premium obuna haqida ma'lumot: Qo‘shimcha imkoniyatlar uchun obuna bo‘ling.")
    elif message.text == "Online 24/7":
        bot.send_message(message.chat.id, "Bot 24/7 faol, har qanday savolingizni yozing.")
    elif message.text == "938839873":
        bot.send_message(message.chat.id, "Bog‘lanish uchun raqam: 938839873")
    else:
        bot.send_message(message.chat.id, "Noto‘g‘ri buyruq. Menyudan tanlang yoki /help ni bering.")

def russian_sections(message):
    if message.text == "Тесты":
        bot.send_message(message.chat.id, "Добро пожаловать в раздел тестов. Скоро добавим тесты.")
    elif message.text == "Словари":
        bot.send_message(message.chat.id, "Раздел словарей: здесь вы найдете необходимые словари.")
    elif message.text == "Книги":
        bot.send_message(message.chat.id, "Раздел книг: список учебников и ссылки для скачивания.")
    elif message.text == "Премиум подписка":
        bot.send_message(message.chat.id, "Информация о премиум подписке: получите дополнительные возможности.")
    elif message.text == "Онлайн 24/7":
        bot.send_message(message.chat.id, "Бот работает 24/7, задавайте вопросы в любое время.")
    elif message.text == "938839873":
        bot.send_message(message.chat.id, "Контактный номер: 938839873")
    else:
        bot.send_message(message.chat.id, "Команда не распознана. Выберите из меню или введите /help.")

@bot.message_handler(commands=['help'])
def help_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        help_text = (
            "Yordam bo‘limi:\n"
            "/start - Botni qayta ishga tushirish\n"
            "/help - Yordamni ko‘rsatish\n"
            "/contact - Aloqa ma'lumotlari\n"
            "/about - Bot haqida qisqacha ma'lumot"
        )
    elif lang == "ru":
        help_text = (
            "Справка:\n"
            "/start - Перезапустить бота\n"
            "/help - Показать помощь\n"
            "/contact - Контактная информация\n"
            "/about - Краткая информация о боте"
        )
    else:
        help_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['contact'])
def contact_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        contact_text = "📞 Aloqa uchun:\n938839873"
    elif lang == "ru":
        contact_text = "📞 Контакты:\n938839873"
    else:
        contact_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, contact_text)

@bot.message_handler(commands=['about'])
def about_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        about_text = "Bu bot testlar, lug‘atlar, kitoblar va premium obuna bo‘limlari bilan ishlaydi."
    elif lang == "ru":
        about_text = "Этот бот работает с разделами тестов, словарей, книг и премиум подписки."
    else:
        about_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, about_text)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        uzbek_sections(message)
    elif lang == "ru":
        russian_sections(message)
    else:
        bot.send_message(message.chat.id, "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала.", reply_markup=language_keyboard())

bot.infinity_polling()
