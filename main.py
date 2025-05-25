import os
from telebot import TeleBot, types

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))

user_language = {}

# Til tanlash klaviaturasi
def language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

# O‘zbekcha asosiy menyu
def main_menu_uz():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ℹ️ Universitet haqida", "📚 Ta’lim yo‘nalishlari")
    markup.add("🎓 O‘quv tizimi", "💰 Grant va stipendiyalar")
    markup.add("🌐 Hamkorlik", "📍Joylashuv")
    markup.add("📞 Aloqa")
    return markup

# Ruscha asosiy menyu
def main_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ℹ️ О университете", "📚 Направления обучения")
    markup.add("🎓 Учебная система", "💰 Гранты и стипендии")
    markup.add("🌐 Сотрудничество", "📍Расположение")
    markup.add("📞 Связь")
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    user_language[message.chat.id] = None
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский"])
def choose_language(message):
    if message.text == "🇺🇿 O‘zbekcha":
        user_language[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Cyber University qabul botiga xush kelibsiz!\nKerakli bo‘limni tanlang:", reply_markup=main_menu_uz())
    else:
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Добро пожаловать в приемную комиссию Cyber University!\nВыберите раздел:", reply_markup=main_menu_ru())

# O‘zbekcha bo‘limlar
def uzbek_sections(message):
    if message.text == "ℹ️ Universitet haqida":
        text = (
            "⚙️ Cyber University — O‘zbekistonning raqamli kelajagiga yo‘l ochuvchi zamonaviy oliy ta’lim dargohi.\n\n"
            "O‘zbekiston Respublikasi Prezidentining 2025-yil 20-yanvardagi PQ–14-sonli qaroriga asosan — Cyber University tashkil etildi.\n\n"
            "Qarorni o‘qing! 🫵 https://lex.uz/uz/docs/-7332592\n\n"
            "🫥 Asosiy maqsad:\n"
            "Cyber University xalqaro raqobatbardosh, innovatsion fikrlovchi va amaliy ko‘nikmaga ega "
            "Kiberxavfsizlik mutaxassislarini tayyorlashga yo‘naltirilgan."
        )
        bot.send_message(message.chat.id, text)

    elif message.text == "📚 Ta’lim yo‘nalishlari":
        text = (
            "📚 *Bakalavriat yo‘nalishlari:*\n"
            "- Kiberxavfsizlik injiniringi: tizimlarni himoya qilish, xavfsizlik strategiyalari.\n"
            "- Kompyuter injiniringi: apparat va dasturiy ta'minotni yaratish.\n"
            "- Dasturiy injiniring: dastur ishlab chiqish va testlash.\n"
            "- Yurisprudensiya: kiber huquq va qonunchilik asoslari.\n"
            "- Menejment: tashkilotlarni boshqarish.\n"
            "- Iqtisodiyot: iqtisodiy tahlil va boshqaruv.\n\n"
            "*Magistratura yo‘nalishlari:*\n"
            "- Axborot xavfsizligi: ilg‘or xavfsizlik tizimlari.\n"
            "- Kiber huquq: kiber jinoyatlar va qonunlar."
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "🎓 O‘quv tizimi":
        text = (
            "🎓 *O‘quv jarayoni xususiyatlari:*\n"
            "- 1 yil Foundation, 3 yil asosiy ta’lim\n"
            "- Ta’lim to‘liq ingliz tilida\n"
            "- Kredit-modul tizimi\n"
            "- Amaliyot IT kompaniyalari va texnoparklarda"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "💰 Grant va stipendiyalar":
        text = (
            "💰 *Imkoniyatlar:*\n"
            "- 2025/2026 o‘quv yili uchun 100 ta davlat granti\n"
            "- Stipendiyalar: sanoat hamkorlari va Innovatsion rivojlanish kengashi orqali"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "🌐 Hamkorlik":
        text = (
            "🌐 *Xalqaro hamkorlik:*\n"
            "- AQSH, Xitoy, Yaponiya kabi davlatlar bilan\n"
            "- Ilg‘or ta’lim dasturlari\n"
            "- Xorijiy mutaxassislar jalb etiladi"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "📍Joylashuv":
        bot.send_message(message.chat.id, "📍 Universitet: Toshkent viloyati, Nurafshon shahri.")

    elif message.text == "📞 Aloqa":
        bot.send_message(message.chat.id,
                         "📞 Aloqa uchun:\n+998 (55) 888-55-55\n+998 95 182 71 17")

    else:
        bot.send_message(message.chat.id, "Noto‘g‘ri buyruq. Menyudan tanlang yoki /help ni bering.")

# Ruscha bo‘limlar
def russian_sections(message):
    if message.text == "ℹ️ О университете":
        text = (
            "⚙️ Cyber University — современное высшее учебное заведение, открывающее путь в цифровое будущее Узбекистана.\n\n"
            "Создан на основании распоряжения Президента Республики Узбекистан № PQ–14 от 20 января 2025 года.\n\n"
            "Читайте распоряжение! 🫵 https://lex.uz/uz/docs/-7332592\n\n"
            "🫥 Основная цель:\n"
            "Подготовка международно конкурентоспособных, инновационно мыслящих и практико-ориентированных специалистов в области кибербезопасности."
        )
        bot.send_message(message.chat.id, text)

    elif message.text == "📚 Направления обучения":
        text = (
            "📚 *Бакалавриат:*\n"
            "- Инженерия кибербезопасности: защита систем и стратегия безопасности.\n"
            "- Компьютерная инженерия: создание аппаратного и программного обеспечения.\n"
            "- Программная инженерия: разработка и тестирование ПО.\n"
            "- Юриспруденция: основы киберзаконов.\n"
            "- Менеджмент: управление организациями.\n"
            "- Экономика: экономический анализ и управление.\n\n"
            "*Магистратура:*\n"
            "- Информационная безопасность: продвинутые системы безопасности.\n"
            "- Киберправо: киберпреступления и законодательство."
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "🎓 Учебная система":
        text = (
            "🎓 *Особенности учебного процесса:*\n"
            "- 1 год Foundation, 3 года основное обучение\n"
            "- Обучение полностью на английском языке\n"
            "- Кредитно-модульная система\n"
            "- Практика в IT-компаниях и технопарках"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "💰 Гранты и стипендии":
        text = (
            "💰 *Возможности:*\n"
            "- 100 государственных грантов на 2025/2026 учебный год\n"
            "- Стипендии от промышленных партнеров и Совета инновационного развития"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "🌐 Сотрудничество":
        text = (
            "🌐 *Международное сотрудничество:*\n"
            "- США, Китай, Япония и другие страны\n"
            "- Продвинутые учебные программы\n"
            "- Привлечение иностранных специалистов"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    elif message.text == "📍Расположение":
        bot.send_message(message.chat.id, "📍 Университет: Ташкентская область, город Нурафшон.")

    elif message.text == "📞 Связь":
        bot.send_message(message.chat.id,
                         "📞 Контакты:\n+998 (55) 888-55-55\n+998 95 182 71 17")

    else:
        bot.send_message(message.chat.id, "Команда не распознана. Выберите из меню или введите /help.")

# Qo‘shimcha buyruqlar uchun handlerlar

@bot.message_handler(commands=['help'])
def help_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        help_text = (
            "Yordam bo‘limi:\n"
            "/start - Botni qayta ishga tushirish\n"
            "/help - Yordamni ko‘rsatish\n"
            "/contact - Aloqa ma'lumotlari\n"
            "/about - Universitet haqida qisqacha ma'lumot"
        )
    elif lang == "ru":
        help_text = (
            "Справка:\n"
            "/start - Перезапустить бота\n"
            "/help - Показать помощь\n"
            "/contact - Контактная информация\n"
            "/about - Краткая информация об университете"
        )
    else:
        help_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['contact'])
def contact_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        contact_text = "📞 Aloqa uchun:\n+998 (55) 888-55-55\n+998 95 182 71 17"
    elif lang == "ru":
        contact_text = "📞 Контакты:\n+998 (55) 888-55-55\n+998 95 182 71 17"
    else:
        contact_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, contact_text)

@bot.message_handler(commands=['about'])
def about_command(message):
    lang = user_language.get(message.chat.id)
    if lang == "uz":
        about_text = (
            "⚙️ Cyber University — O‘zbekistonning raqamli kelajagiga yo‘l ochuvchi zamonaviy oliy ta’lim dargohi.\n"
            "Prezident qarori PQ–14 (2025) asosida tashkil etilgan.\n"
            "Ma'lumot: https://lex.uz/uz/docs/-7332592"
        )
    elif lang == "ru":
        about_text = (
            "⚙️ Cyber University — современное высшее учебное заведение, открывающее путь в цифровое будущее Узбекистана.\n"
            "Создан на основании распоряжения Президента PQ–14 (2025).\n"
            "Информация: https://lex.uz/uz/docs/-7332592"
        )
    else:
        about_text = "Iltimos, avval tilni tanlang / Пожалуйста, выберите язык сначала."
    bot.send_message(message.chat.id, about_text)

# Umumiy handler
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
