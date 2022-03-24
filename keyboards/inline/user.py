from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def inline_user_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("Отмена", callback_data="close"))
    keyboard.insert(InlineKeyboardButton("Продолжить", callback_data="next"))
    return keyboard


def close_inline_user_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Отмена", callback_data="close"))
    return keyboard


def inline_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("Да", callback_data="next"))
    keyboard.insert(InlineKeyboardButton("Нет", callback_data="close"))
    keyboard.add(InlineKeyboardButton("Редактировать первое фото", callback_data="edit_first_photo"))
    keyboard.add(InlineKeyboardButton("Редактировать второе фото", callback_data="edit_second_photo"))
    return keyboard
