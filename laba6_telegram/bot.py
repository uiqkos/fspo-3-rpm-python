import telebot
from html_parser import parse
import requests


def parse_url(url):
    return parse(requests.get(url).text)

def parse_file(file_path):
    return parse(open(file_path, 'r', encoding='utf-8').read())


access_token = '1740470044:AAESOMrnJudl-PDZPahPJIDOF0E9ibyGVOw'
bot = telebot.TeleBot(access_token)

schedules = {
    '2332': parse_file('2332.html')
}

@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text[0] == '/':
        if message.text == '/start':
            return bot.send_message(message.chat.id, 'Для получения расписания введите номер группы ')
        return bot.send_message(message.chat.id, f'"{message.text}"?? \n Нет такой команды :(')

    if message.text in schedules.keys():
        schedule = schedules[message.text]
        return bot.send_message(
            message.chat.id,
            '\n'.join([str(weekday) for weekday in schedule]),
            parse_mode='HTML'
        )

    return bot.send_message(message.chat.id, 'Нет такой группы :(')
