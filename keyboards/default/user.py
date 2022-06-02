from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('Поделиться номером 📱',
                              request_contact=True))
    return markup


def myapps(apps):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for app in apps:
        markup.add(KeyboardButton(app.app_id))
    return markup
