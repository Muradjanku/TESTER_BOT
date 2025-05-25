import telebot

TOKEN = 'SIZNING_BOT_TOKENINGIZ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men botman.")

bot.polling()
