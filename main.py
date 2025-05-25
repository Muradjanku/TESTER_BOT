import os
from telebot import TeleBot, types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))
user_scores = {}
user_steps = {}
user_language = {}
user_data = {}

# Test savollari qisqaroq namunalar
questions_cefr = [
    {"question": "أنا من ــــــ.", "options": ["فرنسا", "أمريكا", "ألمانيا", "مصر"], "answer": "b"},
    {"question": "أنا ــــــ.", "options": ["طالب", "فرنسي", "طبيبة", "مهندس"], "answer": "b"},
    {"question": "هو ــــــ أحمد.", "options": ["يعمل", "اسمه", "عنده", "يسكن"], "answer": "b"},
    {"question": "ــــــ أنت فرنسي؟", "options": ["ما", "هل", "لماذا", "أين"], "answer": "b"},
    {"question": "فاطمة ــــــ ولد.", "options": ["عندها", "عنده", "لديها", "عندهما"], "answer": "a"},
    {"question": "أحمد ــــــ ولد وبنت.", "options": ["عندها", "عنده", "لدي", "لديهما"], "answer": "b"},
    {"question": "بيت أحمد ــــــ.", "options": ["صغير", "جميل", "كبير", "جديد"], "answer": "c"},
    {"question": "ــــــ بيت صغير.", "options": ["هذه", "هذا", "هؤلاء", "هنا"], "answer": "b"},
    {"question": "ــــــ عندي سيارة.", "options": ["لا", "ليس", "لم", "لن"], "answer": "b"},
    {"question": "محمد ــــــ في الجامعة.", "options": ["يدرس", "يعمل", "يسكن", "يذهب"], "answer": "b"},
]

# Qo'shimcha savollarni quyidagilar uchun shunday tuzing (to'ldiring o'zingiz):
questions_at_tanal = questions_cefr * 2  # 20 ta savol uchun namuna (takrorlandi)
questions_arabic_proficiency_30 = questions_cefr * 3  # 30 ta
questions_arabic_proficiency_35 = questions_cefr * 3 + questions_cefr[:5]  # 35 ta
questions_actfl = questions_cefr * 4  # 40 ta

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

def test_type_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("1. CEFR (10 ta test)", callback_data="test_cefr"),
        types.InlineKeyboardButton("2. AT Tanal AL Arabi (20 ta test)", callback_data="test_at_tanal"),
        types.InlineKeyboardButton("3. The Arabic Language Proficiency Test (30 ta test)", callback_data="test_arabic_proficiency"),
        types.InlineKeyboardButton("4. Arabic Proficiency Test (35 ta test)", callback_data="test_arabic_proficiency_35"),
        types.InlineKeyboardButton("5. ACTFL (40 ta test)", callback_data="test_actfl")
    )
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
def start_test(message):
    bot.send_message(message.chat.id, "Test turini tanlang:", reply_markup=test_type_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("test_"))
def test_type_selected(call):
    chat_id = call.message.chat.id
    test_type = call.data

    if test_type == "test_cefr":
        questions_list = questions_cefr
    elif test_type == "test_at_tanal":
        questions_list = questions_at_tanal
    elif test_type == "test_arabic_proficiency":
        questions_list = questions_arabic_proficiency_30
    elif test_type == "test_arabic_proficiency_35":
        questions_list = questions_arabic_proficiency_35
    elif test_type == "test_actfl":
        questions_list = questions_actfl
    else:
        bot.answer_callback_query(call.id, "Noto'g'ri tanlov")
        return

    user_steps[chat_id] = 0
    user_scores[chat_id] = 0
    user_data[chat_id] = {"questions": questions_list}

    bot.answer_callback_query(call.id, "Test boshlandi!")
    send_question(chat_id)

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
    step = user_steps.get(chat_id,
