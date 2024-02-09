import telebot
import requests
from config import bot_token, api_url

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.from_user.id, "👋 Привет! Напиши город и я напишу погоду сейчас!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    city = message.text
    params = {'city': city}

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()

        message_ = f"Погода в городе {city}:\n"
        message_ += f"Температура: {weather_data['temperature']}°C\n"
        message_ += f"Атмосферное давление: {weather_data['pressure']} мм рт.ст.\n"
        message_ += f"Скорость ветра: {weather_data['wind_speed']} м/с"
        bot.send_message(message.from_user.id, message_)

    else:
        bot.send_message(message.from_user.id, 'Такого города нет')


bot.polling(none_stop=True, interval=0)
