import telebot
from html_parser import parse
import requests
import datetime


def parse_url(url):
    return parse(requests.get(url).text)


def parse_file(file_path):
    return parse(open(file_path, 'r', encoding='utf-8').read())


access_token = '1647434653:AAGvqxWnSYIlxtMZ19WFWOytw1DcFzBsLrg'
bot = telebot.TeleBot(access_token)

groups_by_user = {}


def schedule(group):
    url = f'https://itmo.ru/ru/schedule/0/{group.upper()}/schedule.htm'

    reply = parse_url(url)

    if len(reply) == 0:
        return []

    return [str(weekday) for weekday in reply]


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text[0] == '/':
        command, *args = message.text.split()
        if command == '/start' or command == '/help':
            return bot.send_message(
                message.chat.id,
                '/help Показать это сообщение\n'
                '/set {номер группы} Установить номер группы\n'
                '/today Расписание на сегодня для установленной группы\n'
                '/week Расписание на неделю для установленной группы\n'
                '/today {номер группы} Расписание на сегодня для указанной группы\n'
                '/week {номер группы} Расписание на неделю для указанной группы'
            )

        if command == '/set':
            if len(args) == 1:
                groups_by_user[message.chat.id] = args[0]
                return bot.send_message(message.chat.id, 'Текущая группа: ' + groups_by_user[message.chat.id])
            return bot.send_message(message.chat.id, 'Укажите номер группы')

        if groups_by_user[message.chat.id] is None:
            return bot.send_message(
                message.chat.id,
                'Группа не установлена \n '
                'Для установки группы напишите: /set {номер группы}'
            )

        week_schedule = \
            schedule(groups_by_user[message.chat.id]) \
            if len(args) == 0 \
            else schedule(args[0])

        if len(week_schedule) == 0:
            return bot.send_message(message.chat.id, 'Нет такой группы :(')

        if command == '/today':
            return bot.send_message(
                message.chat.id,
                str(week_schedule[datetime.datetime.today().weekday()]),
                parse_mode='HTML'
            )

        if command == '/week':
            return bot.send_message(message.chat.id, '\n'.join(week_schedule), parse_mode='HTML')

        return bot.send_message(message.chat.id, f'"{message.text}"?? \n Нет такой команды :(')

