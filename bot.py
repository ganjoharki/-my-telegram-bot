import telebot
import requests

TELEGRAM_BOT_TOKEN = '8941930891:AAFK0GC5pfacPGQ8Hy-MO_iVTzKy-UOLV7w'

SMM_API_URL = 'https://example-panel.com/api/v2'
SMM_API_KEY = 'API_KEY_HERE'
SERVICE_ID = 100

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "سڵاو! تکایە لینکی پەیجی ئینستاگرام بنێرە:")
    bot.register_next_step_handler(message, get_link)

def get_link(message):
    user_data[message.chat.id]['link'] = message.text
    bot.send_message(message.chat.id, "چەند فۆڵۆوه‌رت دەوێت؟")
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    try:
        quantity = int(message.text)
        link = user_data[message.chat.id]['link']

        bot.send_message(message.chat.id, "داواکارییەکەت لە جێبەجێکردندایە...")

        payload = {
            'key': SMM_API_KEY,
            'action': 'add',
            'service': SERVICE_ID,
            'link': link,
            'quantity': quantity
        }

        response = requests.post(SMM_API_URL, data=payload)
        res_data = response.json()

        if 'order' in res_data:
            bot.send_message(message.chat.id, "سەرکەوتوو بوو!")
        else:
            bot.send_message(message.chat.id, "کێشەیەک هەیە.")

    except ValueError:
        bot.send_message(message.chat.id, "تکایە تەنها ژمارە بنووسە.")

bot.infinity_polling()
