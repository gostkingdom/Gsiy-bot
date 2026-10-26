import os
import telebot
from flask import Flask, request

# Apna BotFather wala token yahan daalein
TOKEN = '8993937365:AAFPQAXEV3Jx90JhJ8A-Ep-71732gu7W5R4'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def is_valid_luhn(card_number: str) -> bool:
    card_number = ''.join(filter(str.isdigit, card_number))
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    digits = [int(d) for d in card_number]
    digits.reverse()
    total_sum = 0
    for idx, digit in enumerate(digits):
        if idx % 2 == 1:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            total_sum += doubled
        else:
            total_sum += digit
    return total_sum % 10 == 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! Mujhe koi bhi number bhejiye, main Luhn algorithm se check karke bataunga ki format valid hai ya nahi.')

@bot.message_handler(func=lambda message: True)
def check_card(message):
    text = message.text.strip()
    if not any(char.isdigit() for char in text):
        bot.reply_to(message, 'Kripya koi valid number bhejiye.')
        return
    if is_valid_luhn(text):
        bot.reply_to(message, '**Valid Format:** Yeh number Luhn algorithm check pass karta hai.')
    else:
        bot.reply_to(message, '**Invalid Format:** Yeh number Luhn algorithm check fail kar gaya.')

# Telegram Webhook Route
@app.route('/' + TOKEN, methods=['POST'])
def telegram_webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

# Setup Webhook Route
@app.route('/')
def setup_webhook():
    bot.remove_webhook()
    render_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://apka-app-name.onrender.com')
    bot.set_webhook(url=render_url + '/' + TOKEN)
    return 'Webhook setup successfully on Render!', 200

if __name__ == '__main__':
    app.run()
