import os
from telebot import TeleBot, types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))

user_scores = {}
user_steps = {}
user_data = {}
user_language = {}

# Test to'plamlari va ularning savollari (namuna uchun qisqaroq ro'yxat)
test_packs = {
    "CEFR (10 ta test)": [
        {"question": "أنا من ــــــ.", "options": ["فرنسا", "أمريكا", "ألمانيا", "مصر"], "answer": "b"},
        {"question": "أنا ــــــ.", "options": ["طالب", "فرنسي", "طبيبة", "مهندس"], "answer": "b"},
        # Qo'shimcha savollar shu yerda...
    ],
    "AT Tanal AL Arabi (20 ta test)": [
        {"question": "سوزان تسكن ــــــ القاهرة.", "options": ["إلى", "في", "على", "مع"], "answer": "b"},
        {"question": "ــــــ تذهب إلى الجامعة كل يوم.", "options": ["هو", "فاطمة", "أنت", "نحن"], "answer": "b"},
        # Qo'shimcha savollar shu yerda...
    ],
    # Boshqa test to'plamlari
}

def language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

def main_menu_uz():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Testni boshlash")
    markup.add("🤖 Bot haqida", "🛠 Xizmatlar")
    markup.add("🎓 O‘quv tizimi", "💎 Premium obuna")
    return markup

def main_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Начать тест")
    markup.add("🤖 О боте", "🛠 Услуги")
    markup.add("🎓 Учебная система", "💎 Премиум подписка")
    return markup

def tests_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for pack_name in test_packs.keys():
        markup.add(pack_name)
    markup.add("⬅️ Orqaga")
    return markup

def calculate_level(score, total):
    percentage = (score / total) * 100 if total else 0
    if percentage >= 95:
        return "C2 (Proficient) — 95-100%", percentage
    elif percentage >= 85:
        return "C1 (Advanced) — 85-90%", percentage
    elif percentage >= 60:
        return "B2 (Upper-Intermediate) — 60-70%", percentage
    elif percentage >= 40:
        return "B1 (Intermediate) — 40-50%", percentage
    elif percentage >= 20:
        return "A2 (Elementary) — 20-25%", percentage
    else:
        return "A1 (Beginner) — 10-15%", percentage

def generate_certificate(name, score, total_questions=40, proficiency_level="Pre-Intermediate (A2)"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    date_str = datetime.now().strftime("%Y-%m-%d")

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "Certificate of Achievement")

    c.setFont("Helvetica", 14)
    text_lines = [
        f"This is to certify that {name}",
        "has completed the Arabic Language Proficiency Quiz",
        f"Date: {date_str}",
        "",
        "Quiz Results:",
        "",
        f"Score: {score} out of {total_questions} questions answered correctly",
        "",
        f"Proficiency Level: {proficiency_level}",
        "",
        "This certificate acknowledges your dedication to learning the Arabic language",
        "and your current proficiency at the assessed level.",
        "Your effort in completing this assessment demonstrates a commitment to improving",
        "your Arabic language skills.",
        "",
        "Issued by: ARABIC TESTER GROUP",
        f"Date: {date_str}"
    ]

    y = height - 150
    for line in text_lines:
        c.drawCentredString(width / 2, y, line)
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@bot.message_handler(commands=['start'])
def start_command(message):
    user_language[message.chat.id] = None
    user_scores[message.chat.id] = 0
    user_steps[message.chat.id] = 0
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Tilni tanlang / Choose language:", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский"])
def language_selected(message):
    if message.text == "🇺🇿 O‘zbekcha":
        user_language[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Assalomu alaykum! Botga xush kelibsiz.", reply_markup=main_menu_uz())
    elif message.text == "🇷🇺 Русский":
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в бот.", reply_markup=main_menu_ru())

@bot.message_handler(func=lambda m: m.text in ["📝 Testni boshlash", "📝 Начать тест"])
def start_test_menu(message):
    if user_language.get(message.chat.id) in ["uz", "ru"]:
        bot.send_message(message.chat.id, "Test to‘plamini tanlang:" if user_language[message.chat.id] == "uz" else "Выберите тест:", reply_markup=tests_menu())
    else:
        bot.send_message(message.chat.id, "Iltimos, tilni tanlang.", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in list(test_packs.keys()) + ["⬅️ Orqaga"])
def test_pack_handler(message):
    chat_id = message.chat.id
    if message.text == "⬅️ Orqaga":
        if user_language.get(chat_id) == "uz":
            bot.send_message(chat_id, "Asosiy menyu:", reply_markup=main_menu_uz())
        else:
            bot.send_message(chat_id, "Главное меню:", reply_markup=main_menu_ru())
        return

    if message.text in test_packs:
        user_data[chat_id] = {
            "test_name": message.text,
            "questions": test_packs[message.text],
            "current_q": 0,
            "score": 0
        }
        send_question(chat_id)

def send_question(chat_id):
    data = user_data.get(chat_id)
    if not data:
        return

    questions = data["questions"]
    current_q = data["current_q"]

    if current_q >= len(questions):
        # Test yakunlandi
        score = data["score"]
        total = len(questions)
        level, percent = calculate_level(score, total)

        if user_language.get(chat_id) == "uz":
            text = (f"Test yakunlandi.\n"
                    f"To‘g‘ri javoblar: {score} / {total}\n"
                    f"Sizning darajangiz: {level}")
        else:
            text = (f"Тест завершен.\n"
                    f"Правильных ответов: {score} / {total}\n"
                    f"Ваш уровень: {level}")

        bot.send_message(chat_id, text)

        # Sertifikat yaratish va yuborish (faqat agar foydalanuvchi ismi bor bo‘lsa)
        try:
            user_name = bot.get_chat(chat_id).first_name or "User"
        except:
            user_name = "User"

        cert_pdf = generate_certificate(user_name, score, total, level)
        bot.send_document(chat_id, cert_pdf, caption="Sertifikat / Сертификат")

        # Test ma'lumotlarini tozalash
        user_data.pop(chat_id, None)
        return

    question = questions[current_q]
    question_text = question["question"]
    options = question["options"]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton(f"{chr(97+i)}) {opt}") for i, opt in enumerate(options)]
    markup.add(*buttons)

    if user_language.get(chat_id) == "uz":
        bot.send_message(chat_id, f"Savol {current_q+1}:\n{question_text}", reply_markup=markup)
    else:
        bot.send_message(chat_id, f"Вопрос {current_q+1}:\n{question_text}", reply_markup=markup)

@bot.message_handler(func=lambda m: user_data.get(m.chat.id) is not None)
def answer_handler(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id)
    if not data:
        return

    current_q = data["current_q"]
    questions = data["questions"]

    if current_q >= len(questions):
        return

    # Javobni tekshirish
    user_answer = message.text.lower().strip()
    correct_answer = questions[current_q]["answer"].lower()

    # Foydalanuvchi javobi "a) ..." ko‘rinishda bo‘ladi, faqat harfni olish kerak
    if len(user_answer) > 0:
        user_answer = user_answer[0]

    if user_answer == correct_answer:
        data["score"] += 1

    data["current_q"] += 1
    user_data[chat_id] = data

    send_question(chat_id)

bot.polling(none_stop=True)
