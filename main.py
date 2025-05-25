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

# Test packs with all questions
test_packs = {
    "CEFR": [
        {"question": "أنا من ــــــ.", "options": ["فرنسا", "أمريكا", "ألمانيا", "مصر"], "answer": "b"},
        {"question": "أنا ــــــ.", "options": ["طالب", "فرنسي", "طبيبة", "مهندس"], "answer": "b"},
        {"question": "هو ــــــ أحمد.", "options": ["يعمل", "اسمه", "عنده", "يسكن"], "answer": "b"},
        {"question": "ــــــ أنت فرنسي؟", "options": ["ما", "هل", "لماذا", "أين"], "answer": "b"},
        {"question": "فاطمة ــــــ ولد.", "options": ["عندها", "عنده", "لديها", "عندهما"], "answer": "a"},
    ],
    "AT Tanal AL Arabi": [
        {"question": "أحمد ــــــ ولد وبنت.", "options": ["عندها", "عنده", "لدي", "لديهما"], "answer": "b"},
        {"question": "بيت أحمد ــــــ.", "options": ["صغير", "جميل", "كبير", "جديد"], "answer": "c"},
        {"question": "ــــــ بيت صغير.", "options": ["هذه", "هذا", "هؤلاء", "هنا"], "answer": "b"},
        {"question": "ــــــ عندي سيارة.", "options": ["لا", "ليس", "لم", "لن"], "answer": "b"},
        {"question": "محمد ــــــ في الجامعة.", "options": ["يدرس", "يعمل", "يسكن", "يذهب"], "answer": "b"},
    ],
    "The Arabic Language Proficiency Test": [
        {"question": "سوزان تسكن ــــــ القاهرة.", "options": ["إلى", "في", "على", "مع"], "answer": "b"},
        {"question": "ــــــ تذهب إلى الجامعة كل يوم.", "options": ["هو", "فاطمة", "أنت", "نحن"], "answer": "b"},
        {"question": "ــــــ تذهب إلى الجامعة؟", "options": ["أين", "كيف", "متى", "لماذا"], "answer": "c"},
        {"question": "أحمد ذهب إلى الجامعة ــــــ.", "options": ["غدًا", "أمس", "الآن", "سابقًا"], "answer": "b"},
        {"question": "فاطمة ستزور سوزان ــــــ informasjon.", "options": ["البارحة", "غدًا", "اليوم", "أمس"], "answer": "b"},
    ],
    "Arabic Proficiency Test": [
        {"question": "أنا أعود ــــــ البيت الساعة الخامسة.", "options": ["من", "إلى", "في", "عن"], "answer": "b"},
        {"question": "زار صديقه ــــــ ذهب إلى السوق.", "options": ["قبل أن", "بعد أن", "حينما", "لأن"], "answer": "b"},
        {"question": "سأنام بعد أن ــــــ الفيلم.", "options": ["شاهدت", "أشاهد", "سأشاهد", "مشاهدة"], "answer": "b"},
        {"question": "أريد ــــــ أشتري سيارة جديدة.", "options": ["حتى", "أن", "لأن", "لكن"], "answer": "b"},
        {"question": "هم يحبون أن ــــــ اللغة العربية.", "options": ["يدرس", "يدرسوا", "دراسة", "درسوا"], "answer": "b"},
    ],
    "American Council on the Teaching of Foreign Languages (ACTFL)": [
        {"question": "نمت مبكرًا ــــــ أصحو مبكرًا.", "options": ["لأن", "حتى", "لكي", "إذا"], "answer": "c"},
        {"question": "كنت طالبًا وــــــ مدرسًا.", "options": ["صرت", "أصبحت", "ظللت", "عدت"], "answer": "b"},
        {"question": "قرأت أربعة ــــــ خلال الإجازة.", "options": ["كتاب", "كتب", "كتابًا", "كُتُبًا"], "answer": "b"},
        {"question": "غادرت القاهرة ولم ــــــ أسكن فيها.", "options": ["أعد", "أعود", "أرجع", "أذهب"], "answer": "a"},
        {"question": "بدأت العمل ــــــ.", "options": ["مسرورًا", "سعيد", "فرحان", "السرور"], "answer": "a"},
    ],
    "A1": [
        {"question": "كتاب عرب tilida qanday?", "options": ["كتاب", "قلم", "مكتب", "بلا"], "answer": "a"},
        {"question": "سلام so‘zining arab tilidagi tarjimasi qaysi?", "options": ["وداعا", "مرحبا", "شكرا", "بلا"], "answer": "b"},
        {"question": "To‘g‘ri gapni tanlang: أنا ___ طالب.", "options": ["كتب", "طالب", "مدرسة", "بلا"], "answer": "b"},
        {"question": "Uy arab tilida nima?", "options": ["بيت", "شارع", "سيارة", "بلا"], "answer": "a"},
        {"question": "Rahmat arab tilida qanday?", "options": ["شكرا", "نعم", "لا", "بلا"], "answer": "a"},
        {"question": "Bola ko‘plik shakli qaysi?", "options": ["أولاد", "ولدات", "ولدون", "بلا"], "answer": "a"},
        {"question": "Xayrli tong arab tilida qanday?", "options": ["صباح الخير", "مساء الخير", "تصبح على خير", "بلا"], "answer": "a"},
        {"question": "Bo‘sh joyni to‘ldiring: هو ___ في المدرسة.", "options": ["يدرس", "يكتب", "يلعب", "بلا"], "answer": "a"},
        {"question": "Men suv ichaman arab tilida qanday?", "options": ["أنا أشرب ماء", "أنا أقرأ كتاب", "أنا أذهب إلى المدرسة", "بلا"], "answer": "a"},
        {"question": "Qizil so‘zining arab tilidagi tarjimasi qaysi?", "options": ["أحمر", "أزرق", "أخضر", "بلا"], "answer": "a"},
        {"question": "Qalam arab tilida qanday?", "options": ["كتاب", "قلم", "مكتب", "بلا"], "answer": "b"},
        {"question": "Do‘st arab tilida qanday?", "options": ["صديق", "أستاذ", "معلم", "بلا"], "answer": "a"},
        {"question": "Non arab tilida qanday?", "options": ["خبز", "ماء", "تفاح", "بلا"], "answer": "a"},
        {"question": "Ular arab tilida qanday?", "options": ["هم", "أنا", "أنت", "بلا"], "answer": "a"},
        {"question": "Katta arab tilida qanday?", "options": ["صغير", "كبير", "طويل", "بلا"], "answer": "b"},
        {"question": "Uyda arab tilida qanday?", "options": ["في المدرسة", "في البيت", "في السوق", "بلا"], "answer": "b"},
        {"question": "Men kitob o‘qiyman arab tilida qanday?", "options": ["أنا أكتب كتاب", "أنا أقرأ كتاب", "أنا أشرب ماء", "بلا"], "answer": "b"},
        {"question": "Qiz arab tilida qanday?", "options": ["ولد", "بنت", "رجل", "بلا"], "answer": "b"},
        {"question": "Suv arab tilida qanday?", "options": ["ماء", "نار", "هواء", "بلا"], "answer": "a"},
        {"question": "Yaxshi arab tilida qanday?", "options": ["جيد", "سيئ", "ضعيف", "بلا"], "answer": "a"},
        {"question": "Yoz arab tilida qanday?", "options": ["شتاء", "صيف", "ربيع", "بلا"], "answer": "b"},
        {"question": "Erkak arab tilida qanday?", "options": ["رجل", "امرأة", "طفل", "بلا"], "answer": "a"},
        {"question": "Maktab arab tilida qanday?", "options": ["مدرسة", "جامعة", "مستشفى", "بلا"], "answer": "a"},
        {"question": "Men yaxshi ko‘raman arab tilida qanday?", "options": ["أنا أحب", "أنا أكره", "أنا أذهب", "بلا"], "answer": "a"},
        {"question": "Daraxt arab tilida qanday?", "options": ["شجرة", "زهرة", "نهر", "بلا"], "answer": "a"},
        {"question": "Qora arab tilida qanday?", "options": ["أسود", "أبيض", "أحمر", "بلا"], "answer": "a"},
        {"question": "U qiz arab tilida qanday?", "options": ["هو ولد", "هي بنت", "هو رجل", "بلا"], "answer": "b"},
        {"question": "Do‘kon arab tilida qanday?", "options": ["سوق", "مدرسة", "مكتب", "بلا"], "answer": "a"},
        {"question": "Men o‘qiyman arab tilida qanday?", "options": ["أنا أكتب", "أنا أقرأ", "أنا أشرب", "بلا"], "answer": "b"},
        {"question": "Tez arab tilida qanday?", "options": ["بطيء", "سريع", "طويل", "بلا"], "answer": "b"},
        {"question": "Kichik arab tilida qanday?", "options": ["كبير", "صغير", "طويل", "بلا"], "answer": "b"},
        {"question": "Qizil arab tilida qanday?", "options": ["أحمر", "أزرق", "أصفر", "بلا"], "answer": "a"},
        {"question": "Ona arab tilida qanday?", "options": ["أم", "أب", "أخ", "بلا"], "answer": "a"},
        {"question": "Men yaxshi ko‘raman arab tilida qanday?", "options": ["أنا أحب", "أنا أكره", "أنا أذهب", "بلا"], "answer": "a"},
        {"question": "Uzoq arab tilida qanday?", "options": ["قريب", "بعيد", "طويل", "بلا"], "answer": "b"},
        {"question": "Yosh arab tilida qanday?", "options": ["صغير", "كبير", "طويل", "بلا"], "answer": "a"},
        {"question": "Boshqaruvchi arab tilida qanday?", "options": ["مدير", "معلم", "طالب", "بلا"], "answer": "a"},
        {"question": "Bosh arab tilida qanday?", "options": ["رأس", "يد", "قدم", "بلا"], "answer": "a"},
        {"question": "Do‘stlik arab tilida qanday?", "options": ["صداقة", "عداوة", "حب", "بلا"], "answer": "a"},
        {"question": "Kitoblar arab tilida qanday?", "options": ["كتب", "كتاب", "مكتبة", "بلا"], "answer": "a"},
        {"question": "Ular o‘qiyapti arab tilida qanday?", "options": ["هم يكتبون", "هم يقرؤون", "هم يلعبون", "بلا"], "answer": "b"},
        {"question": "Men o‘tiraman arab tilida qanday?", "options": ["أنا أقف", "أنا أجلس", "أنا أمشي", "بلا"], "answer": "b"},
        {"question": "Qora qalam arab tilida qanday?", "options": ["قلم أسود", "قلم أحمر", "قلم أزرق", "بلا"], "answer": "a"},
        {"question": "Yosh bola arab tilida qanday?", "options": ["ولد صغير", "ولد كبير", "رجل صغير", "بلا"], "answer": "a"},
        {"question": "Kitob juda qiziqarli arab tilida qanday?", "options": ["الكتاب ممتع جداً", "الكتاب ممل جداً", "الكتاب كبير جداً", "بلا"], "answer": "a"},
        {"question": "Qalampir arab tilida qanday?", "options": ["فلفل", "ملح", "سكر", "بلا"], "answer": "a"},
        {"question": "Qalam va daftar arab tilida qanday?", "options": ["قلم و دفتر", "كتاب و مكتب", "سيارة و شارع", "بلا"], "answer": "a"},
        {"question": "Men ovqat yeyman arab tilida qanday?", "options": ["أنا أشرب ماء", "أنا أقرأ كتاب", "أنا أكل طعام", "بلا"], "answer": "c"},
        {"question": "Yaqin do‘st arab tilida qanday?", "options": ["صديق قريب", "صديق بعيد", "صديق جديد", "بلا"], "answer": "a"},
        {"question": "Men uydaman arab tilida qanday?", "options": ["أنا في المدرسة", "أنا في البيت", "أنا في السوق", "بلا"], "answer": "b"},
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

def education_system_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    for level in levels:
        markup.add(level)
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
        bot.send_message(message.chat.id, 
                         "Test to'plamini tanlang:" if user_language[message.chat.id] == "uz" else "Выберите тест:", 
                         reply_markup=tests_menu())
    else:
        bot.send_message(message.chat.id, "Iltimos, tilni tanlang.", reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🎓 O‘quv tizimi", "🎓 Учебная система"])
def education_system_handler(message):
    chat_id = message.chat.id
    if user_language.get(chat_id) == "uz":
        bot.send_message(chat_id, "Darajani tanlang:", reply_markup=education_system_menu())
    else:
        bot.send_message(chat_id, "Выберите уровень:", reply_markup=education_system_menu())

@bot.message_handler(func=lambda m: m.text in ["A1", "A2", "B1", "B2", "C1", "C2", "⬅️ Orqaga"])
def level_handler(message):
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
    else:
        bot.send_message(chat_id, 
                         f"{message.text} testi hozircha mavjud emas." if user_language.get(chat_id) == "uz" else f"Тест {message.text} пока недоступен.")

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
        # Test completed
        score = data["score"]
        total = len(questions)
        level, percent = calculate_level(score, total)

        if user_language.get(chat_id) == "uz":
            text = (f"Test yakunlandi.\n"
                    f"To'g'ri javoblar: {score} / {total}\n"
                    f"Sizning darajangiz: {level}")
        else:
            text = (f"Тест завершен.\n"
                    f"Правильных ответов: {score} / {total}\n"
                    f"Ваш уровень: {level}")

        bot.send_message(chat_id, text)

        # Generate certificate
        try:
            user_name = bot.get_chat(chat_id).first_name or "User"
        except:
            user_name = "User"

        cert_pdf = generate_certificate(user_name, score, total, level)
        bot.send_document(chat_id, cert_pdf, caption="Sertifikat / Сертификат")

        # Clear test data
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

    # Check answer
    user_answer = message.text.lower().strip()
    correct_answer = questions[current_q]["answer"].lower()

    # Extract just the letter (a/b/c/d)
    if len(user_answer) > 0:
        user_answer = user_answer[0]

    if user_answer == correct_answer:
        data["score"] += 1

    data["current_q"] += 1
    user_data[chat_id] = data

    send_question(chat_id)

bot.polling(none_stop=True)
