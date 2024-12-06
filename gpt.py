import telebot
from settings import API_TOKEN
import webbrowser
import random

bot = telebot.TeleBot(API_TOKEN)

users_list = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Зарегистрируйся с помощью команды /register http://127.0.0.1:5000!")

@bot.message_handler(commands=['register'])
def register(message):
    webbrowser.open('http://127.0.0.1:5000')
    bot.reply_to(message, 'Чтобы войти в чат, введите команду /chat')

@bot.message_handler(commands=['chat'])
def chat(message):
    user_id = message.from_user.id
    if user_id not in users_list:
        with open('yes_or_no.txt', 'r') as yes_file:
            yes = yes_file.read().strip()
        
        if yes == 'Yes':
            users_list.append(user_id)
            bot.reply_to(message, "Вы успешно зарегистрированы! Теперь вы можете отправлять сообщения.")
        else:
            bot.reply_to(message, 'Неверный пароль!')
    else:
        bot.reply_to(message, "Вы уже зарегистрированы!")

@bot.message_handler(func=lambda message: True)
def send_message_to_random_user(message):
    text_user = str(message.text)
    if not users_list:
        bot.reply_to(message, "Нет зарегистрированных пользователей.")
        return
    
    random_user = random.choice(users_list)
    bot.send_message(random_user, text_user)
    bot.reply_to(message, f"Сообщение отправлено пользователю с ID {random_user}.")

bot.infinity_polling()