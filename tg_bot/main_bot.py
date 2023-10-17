import telebot
import requests
import json
from decouple import config

bot = telebot.TeleBot(config('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    item = telebot.types.InlineKeyboardButton("Click to see anime", callback_data='show_anime')
    markup.add(item)
    bot.reply_to(message, 'Hello, AniSlime API welcomes you, glad to help you!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_anime')
def send_title_anime(call):
    res = requests.get('http://34.89.235.149/api/v1/title/')
    data = json.loads(res.content)
    titles = data.get('results')
    number = 0
    for i in titles:
        number += 1
        bot.send_message(call.message.chat.id, f'Аниме по популярности {number}: \n{i.get("name")}')



if __name__ == '__main__':
    bot.polling()
