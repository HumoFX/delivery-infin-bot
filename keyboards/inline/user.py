from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_builder import ApplicationCB


def inline_user_keyboard(app_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("Отмена", callback_data=ApplicationCB.action.new(action="close",
                                                                                          value=app_id)))
    keyboard.insert(InlineKeyboardButton("Продолжить", callback_data=ApplicationCB.action.new(action="next",
                                                                                              value=app_id)))
    return keyboard


def inline_end_keyboard(app_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("Отмена", callback_data=ApplicationCB.action.new(action="close",
                                                                                          value=app_id)))
    keyboard.insert(InlineKeyboardButton("Завершить", callback_data=ApplicationCB.action.new(action="next",
                                                                                             value=app_id)))
    return keyboard


def close_inline_user_keyboard(app_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Отмена", callback_data=ApplicationCB.action.new(action="close", value=app_id)))
    return keyboard


def inline_confirm_keyboard(app_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("Да", callback_data=ApplicationCB.action.new(action="next",
                                                                                      value=app_id)))
    keyboard.insert(InlineKeyboardButton("Нет", callback_data=ApplicationCB.action.new(action="close",
                                                                                       value=app_id)))
    keyboard.add(InlineKeyboardButton("Редактировать первое фото",
                                      callback_data=ApplicationCB.action.new(action="edit_first_photo",
                                                                             value=app_id)))
    keyboard.add(InlineKeyboardButton("Редактировать второе фото",
                                      callback_data=ApplicationCB.action.new(action="edit_second_photo",
                                                                             value=app_id)))
    return keyboard
