import telebot
from telebot import types
from config import telegram_token
from weatherz import get_weather

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=["start"])  # декоратор
def start(message):  # Название функции не играет никакой роли
    mess = f'Привет, <b>{message.from_user.first_name}!</b> ' \
           f'Напиши мне название города и я пришлю тебе текущую сводку погоды!' # выводит имя пользователя
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types=["text"])
def weather(message):
    bot.send_message(message.chat.id, get_weather(message.text), parse_mode='html')






bot.polling(none_stop=True)