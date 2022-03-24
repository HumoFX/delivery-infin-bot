from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('Отправить контакт',
                              request_contact=True))
    return markup

