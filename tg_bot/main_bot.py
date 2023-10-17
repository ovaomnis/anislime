import telebot
import requests
import json
from decouple import config

bot = telebot.TeleBot(config('TELEGRAM_BOT_TOKEN'))
current_page = 1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    item = telebot.types.InlineKeyboardButton("Click to see anime", callback_data='show_anime')
    markup.add(item)
    bot.reply_to(message, 'Hello, AniSlime API welcomes you, glad to help you!', reply_markup=markup)


def load_anime_from_page(page, chat_id):
    res = requests.get(f'http://34.89.235.149/api/v1/title/?page={page}')
    data = json.loads(res.content)
    data_next = data.get('next')
    titles = data.get('results')

    for index, anime in enumerate(titles, 1):
        anime_name = anime.get("name")
        bot.send_message(chat_id, f'{anime_name}')

    if data_next:
        markup = telebot.types.InlineKeyboardMarkup()
        item = telebot.types.InlineKeyboardButton("Click to see next page of anime", callback_data='show_next_page')
        markup.add(item)
        bot.send_message(chat_id, "Доступна следующая страница с аниме:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_anime')
def send_title_anime(call):
    global current_page

    load_anime_from_page(current_page, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'show_next_page')
def show_next_page(call):
    global current_page
    current_page += 1

    load_anime_from_page(current_page, call.message.chat.id)


if __name__ == '__main__':
    bot.polling()
