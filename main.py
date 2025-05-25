import os
from telebot import TeleBot, types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))
user_language = {}
user_scores = {}

# Til tanlash klaviaturasi
def language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

# O‘zbekcha menyu
def main_menu_uz():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Testni boshlash")
    markup.add("🤖 Bot haqida", "🛠 Xizmatlar")
    markup.add("🎓 O‘quv tizimi", "💎 Premium obuna")
    return markup

# Sertifikat yaratish funksiyasi
def generate_certificate(name, score):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "RAHMATNOMA")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 150, f"Ismi: {name}")
    c.drawCentredString(width / 2, height - 180, f"Arab tili testidan {score}% natija olganingiz uchun")
    c.drawCentredString(width / 2, height - 210, "rahmat bildiramiz!")

    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, height - 300, "Arabic Tester jamoasi")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# /start komandasi
@bot.message_handler(commands=['start'])
def start_command(message):
    user_language[message.chat.id] = None
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())

# Til tanlanganda
@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский"])
def choose_language(message):
    if message.text == "🇺🇿 O‘zbekcha":
        user_language[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Arabic Tester botiga xush kelibsiz!", reply_markup=main_menu_uz())
    else:
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Добро пожаловать в Arabic Tester бот!", reply_markup=main_menu_uz())

# Test boshlash
@bot.message_handler(func=lambda m: m.text == "📝 Testni boshlash")
def start_test(message):
    question = "1-savol: 'Salom' arab tilida qanday?\nA) Marhaban\nB) Shukran\nC) Kitab"
    bot.send_message(message.chat.id, question)
    user_scores[message.chat.id] = {"score": 0, "step": 1}

@bot.message_handler(func=lambda m: m.chat.id in user_scores)
def handle_test(message):
    progress = user_scores[message.chat.id]
    step = progress["step"]

    if step == 1:
        if message.text.lower().startswith("a"):
            progress["score"] += 1
        bot.send_message(message.chat.id, "2-savol: 'Rahmat' arab tilida qanday?\nA) Shukran\nB) Afwan\nC) Sabah")
        progress["step"] = 2

    elif step == 2:
        if message.text.lower().startswith("a"):
            progress["score"] += 1
        bot.send_message(message.chat.id, "Test yakunlandi. Natijangiz hisoblanmoqda...")
        total = 2
        correct = progress["score"]
        percent = int((correct / total) * 100)

        name = message.from_user.first_name or "Foydalanuvchi"

        if percent >= 60:
            pdf = generate_certificate(name, percent)
            bot.send_document(message.chat.id, pdf, caption=f"Tabriklaymiz! Siz {percent}% natija oldingiz.")
        else:
            bot.send_message(message.chat.id, f"Siz {percent}% oldingiz. Kamida 60% talab qilinadi.")

        del user_scores[message.chat.id]

bot.infinity_polling()
