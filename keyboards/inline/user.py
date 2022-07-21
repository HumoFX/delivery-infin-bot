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


def inline_approve_in_group_keyboard(app_id, app_name, msg_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("❌Отклонить", callback_data=ApplicationCB.in_group.new(act="reject",
                                                                                                val=app_id,
                                                                                                app_id=app_name,
                                                                                                msg=msg_id)))
    keyboard.insert(InlineKeyboardButton("✅Подтвердить", callback_data=ApplicationCB.in_group.new(act="approve",
                                                                                                  val=app_id,
                                                                                                  app_id=app_name,
                                                                                                  msg=msg_id)))
    return keyboard


def inline_approve_confirm_in_group_keyboard(app_id, app_name, msg_id, approve):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("⬅️Назад",
                                         callback_data=ApplicationCB.in_group_confirmation.new(act="back",
                                                                                               val=app_id,
                                                                                               app_id=app_name,
                                                                                               msg=msg_id)))
    if approve:
        keyboard.insert(
            InlineKeyboardButton("✅Подтвердить", callback_data=ApplicationCB.in_group_confirmation.new(act="approve",
                                                                                                       val=app_id,
                                                                                                       app_id=app_name,
                                                                                                       msg=msg_id)))
    else:
        keyboard.insert(InlineKeyboardButton("🚫Отклонить",
                                             callback_data=ApplicationCB.in_group_confirmation.new(act="reject",
                                                                                                   val=app_id,
                                                                                                   app_id=app_name,
                                                                                                   msg=msg_id)))

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
