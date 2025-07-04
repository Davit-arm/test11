import telebot # библиотека telebot
from config import token # импорт токена
from telebot.types import ChatPermissions
import time

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: message.text.startswith('https://'))
def url_ban(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.ban_chat_member(chat_id, user_id)
        bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    
@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, "im a bot that can ban people")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['mute'])
def mute(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id

        until_date = int(time.time()) + 3600

        permissions = ChatPermissions(can_send_messages=False)

        bot.restrict_chat_member(chat_id, user_id, permissions=permissions, until_date=until_date)
        bot.reply_to(message, "Пользователь замьючен на 1 час.")
    else:
        bot.reply_to(message, "Эта команда работает только в ответ на сообщение.")

bot.infinity_polling(none_stop=True)
