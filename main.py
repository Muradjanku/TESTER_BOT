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
        {"question": "أنا ــــــ.", "options": ["طالب", "فرنسي", "طبيبة", "مهندس"], "answer": "b"},
        {"question": "هو ــــــ أحمد.", "options": ["يعمل", "اسمه", "عنده", "يسكن"], "answer": "b"},
        {"question": "ــــــ أنت فرنسي؟", "options": ["ما", "هل", "لماذا", "أين"], "answer": "b"},
        {"question": "فاطمة ــــــ ولد.", "options": ["عندها", "عنده", "لديها", "عندهما"], "answer": "a"},
        {"question": "أحمد ــــــ ولد وبنت.", "options": ["عندها", "عنده", "لدي", "لديهما"], "answer": "b"},
        {"question": "بيت أحمد ــــــ.", "options": ["صغير", "جميل", "كبير", "جديد"], "answer": "c"},
        {"question": "ــــــ بيت صغير.", "options": ["هذه", "هذا", "هؤلاء", "هنا"], "answer": "b"},
        {"question": "ــــــ عندي سيارة.", "options": ["لا", "ليس", "لم", "لن"], "answer": "b"},
        {"question": "محمد ــــــ في الجامعة.", "options": ["يدرس", "يعمل", "يسكن", "يذهب"], "answer": "b"},
    ],
    "AT Tanal AL Arabi (20 ta test)": [
        {"question": "سوزان تسكن ــــــ القاهرة.", "options": ["إلى", "في", "على", "مع"], "answer": "b"},
        {"question": "ــــــ تذهب إلى الجامعة كل يوم.", "options": ["هو", "فاطمة", "أنت", "نحن"], "answer": "b"},
        {"question": "ــــــ تذهب إلى الجامعة؟", "options": ["أين", "كيف", "متى", "لماذا"], "answer": "c"},
        {"question": "أحمد ذهب إلى الجامعة ــــــ.", "options": ["غدًا", "أمس", "الآن", "سابقًا"], "answer": "b"},
        {"question": "فاطمة ستزور سوزان ــــــ.", "options": ["البارحة", "غدًا", "اليوم", "أمس"], "answer": "b"},
        {"question": "محمد ــــــ يذهب إلى العمل غدًا.", "options": ["لا", "لن", "لم", "ما"], "answer": "b"},
        {"question": "هم ــــــ يسافرون الأسبوع القادم.", "options": ["قد", "سوف", "كان", "لن"], "answer": "b"},
        {"question": "نحن سافرنا الأسبوع ــــــ.", "options": ["الحالي", "الماضي", "القادم", "الجديد"], "answer": "b"},
        {"question": "فاطمة ــــــ صديقتها أمس.", "options": ["تزور", "زارت", "ستزور", "زوروا"], "answer": "b"},
        {"question": "أحمد ــــــ يزر صديقه أمس.", "options": ["ما", "لم", "لا", "لن"], "answer": "b"},
        {"question": "أنا أعود ــــــ البيت الساعة الخامسة.", "options": ["من", "إلى", "في", "عن"], "answer": "b"},
        {"question": "زار صديقه ــــــ ذهب إلى السوق.", "options": ["قبل أن", "بعد أن", "حينما", "لأن"], "answer": "b"},
        {"question": "سأنام بعد أن ــــــ الفيلم.", "options": ["شاهدت", "أشاهد", "سأشاهد", "مشاهدة"], "answer": "b"},
        {"question": "أريد ــــــ أشتري سيارة جديدة.", "options": ["حتى", "أن", "لأن", "لكن"], "answer": "b"},
        {"question": "هم يحبون أن ــــــ اللغة العربية.", "options": ["يدرس", "يدرسوا", "دراسة", "درسوا"], "answer": "b"},
        {"question": "هذه صديقتي ــــــ تدرس في الجامعة.", "options": ["الذي", "التي", "الذين", "اللواتي"], "answer": "b"},
        {"question": "أين الكتب التي ــــــ أمس؟", "options": ["اشترىتموها", "اشتريتها", "تشتريها", "شراؤها"], "answer": "b"},
        {"question": "أنا أدرس العربية ــــــ صديقي فيدرس الفرنسية.", "options": ["لكن", "أما", "لأن", "أو"], "answer": "b"},
        {"question": "لا أحب ــــــ إلى السوق.", "options": ["الذهاب", "أذهب", "ذهبت", "سيذهب"], "answer": "a"},
        {"question": "عدت إلى البيت بعد ــــــ صديقي.", "options": ["مقابلة", "قابلت", "سأقابل", "لقاء"], "answer": "a"},
    ],
    "The Arabic Language Proficiency Test (30 ta test)": [
        {"question": "نمت مبكرًا ــــــ أصحو مبكرًا.", "options": ["لأن", "حتى", "لكي", "إذا"], "answer": "c"},
        {"question": "كنت طالبًا وــــــ مدرسًا.", "options": ["صرت", "أصبحت", "ظليت", "عدت"], "answer": "b"},
        {"question": "قرأت أربعة ــــــ خلال الإجازة.", "options": ["كتاب", "كتب", "كتابًا", "كُتُبًا"], "answer": "b"},
        {"question": "غادرت القاهرة ولم ــــــ أسكن فيها.", "options": ["أعد", "أعود", "أرجع", "أذهب"], "answer": "a"},
        {"question": "بدأت العمل ــــــ.", "options": ["مسرورًا", "سعيد", "فرحان", "السرور"], "answer": "a"},
        {"question": "انتشر الخبر ــــــ واسعًا.", "options": ["انتشارًا", "منتشرًا", "ينتشر", "انتشار"], "answer": "a"},
        {"question": "توقفت عن التدخين ــــــ من الأمراض.", "options": ["خوفًا", "خائفًا", "الخوف", "أخاف"], "answer": "a"},
        {"question": "ــــــ علمت أنك مريض لزرتك.", "options": ["لو", "إذا", "لولا", "لكن"], "answer": "a"},
        {"question": "ــــــ الطبيب لمات المريض.", "options": ["إذا", "لولا", "لو", "لكن"], "answer": "b"},
        {"question": "هو يعيش سعيدًا على الرغم من ــــــ.", "options": ["تعبه", "فقره", "مرضه", "مشاكله"], "answer": "b"},
        # 20 ta savol qo'shishingiz mumkin shu yerda
    ],
    "Arabic Proficiency Test (35 ta test)": [
        # Siz berilgan savollarni shu yerga joylashtiring
    ],
    "American Council on the Teaching of Foreign Languages (ACTFL) (40 ta test)": [
        # Siz berilgan savollarni shu yerga joylashtiring
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
        user_language[message.chat.id] = "
