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

# Test to'plamlari va ularning savollari
test_packs = {
    "CEFR (10 ta test)": [
        {"question": "أنا من ــــــ.", "options": ["فرنسا", "أمريكا", "ألمانيا", "مصر"], "answer": "b"},
        # Qo'shimcha 9 ta savol shu yerda bo'lishi kerak
    ],
    "AT Tanal AL Arabi (20 ta test)": [
        # 20 ta savol shu yerda
    ],
    "The Arabic Language Proficiency Test (30 ta test)": [
        # 30 ta savol shu yerda
    ],
    "Arabic Proficiency Test (35 ta test)": [
        # 35 ta savol shu yerda
    ],
    "American Council on the Teaching of Foreign Languages (ACTFL) (40 ta test)": [
        # 40 ta savol shu yerda
    ]
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

def tests_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for pack_name in test_packs.keys():
        markup.add(pack_name)
    markup.add("⬅️ Orqaga")
    return markup

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

def calculate_level(score, total):
    percentage = (score / total) * 100
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
        bot.send_message(message.chat.id, "Arabic Tester botiga xush kelibsiz!", reply_markup=main_menu_uz())
    else:
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Добро пожаловать в Arabic Tester бот!", reply_markup=main_menu_uz())

@bot.message_handler(func=lambda m: m.text == "📝 Testni boshlash")
def start_test_menu(message):
    bot.send_message(message.chat.id, "Test to‘plamini tanlang:", reply_markup=tests_menu())

@bot.message_handler(func=lambda m: m.text in test_packs.keys())
def select_test_pack(message):
    chat_id = message.chat.id
    selected_pack = message.text
    user_data[chat_id]["questions"] = test_packs[selected_pack]
    user_scores[chat_id] = 0
    user_steps[chat_id] = 0
    bot.send_message(chat_id, f"Test boshlandi: {selected_pack}\nHar bir savolga faqat a, b, c, yoki d deb javob bering.")
    send_question(chat_id)

@bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
def back_to_main_menu(message):
    bot.send_message(message.chat.id, "Asosiy menyu", reply_markup=main_menu_uz())

def send_question(chat_id):
    step = user_steps.get(chat_id, 0)
    questions_list = user_data.get(chat_id, {}).get("questions", [])
    if step < len(questions_list):
        q = questions_list[step]
        options_text = "\n".join([f"{chr(97+i)}) {opt}" for i, opt in enumerate(q["options"])])
        bot.send_message(chat_id, f"{step+1}-savol:\n{q['question']}\n{options_text}")
    else:
        finish_test(chat_id)

@bot.message_handler(func=lambda m: m.chat.id in user_steps)
def handle_answer(message):
    chat_id = message.chat.id
    step = user_steps.get(chat_id, 0)
    questions_list = user_data.get(chat_id, {}).get("questions", [])

    if step >= len(questions_list):
        bot.send_message(chat_id, "Test yakunlandi.")
        return

    user_answer = message.text.strip().lower()
    correct_answer = questions_list[step]["answer"].lower()

    if user_answer in ['a', 'b', 'c', 'd']:
        if user_answer == correct_answer:
            user_scores[chat_id] = user_scores.get(chat_id, 0) + 1

        user_steps[chat_id] = step + 1

        if user_steps[chat_id] < len(questions_list):
            send_question(chat_id)
        else:
            bot.send_message(chat_id, "Test yakunlandi. Ismingizni kiriting, sertifikat yaratamiz:")
            bot.register_next_step_handler(message, generate_and_send_certificate)
    else:
        bot.send_message(chat_id, "Iltimos, faqat a, b, c yoki d variantlaridan birini kiriting.")

def generate_and_send_certificate(message):
    chat_id = message.chat.id
    name = message.text.strip() or "Foydalanuvchi"
    score = user_scores.get(chat_id, 0)
    total_questions = len(user_data.get(chat_id, {}).get("questions", []))
    proficiency_level, _ = calculate_level(score, total_questions)

    certificate_pdf = generate_certificate(name, score, total_questions, proficiency_level)
    bot.send_document(chat_id, certificate_pdf)

    user_scores.pop(chat_id, None)
    user_steps.pop(chat_id, None)
    user_data.pop(chat_id, None)

bot.infinity_polling()
