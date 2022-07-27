from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_builder import ApplicationCB
from utils.constants import PAGINATION


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


def pagination_inline_button(count, offset, limit, page):
    markup = InlineKeyboardMarkup(row_width=2)
    if offset > 0:
        markup.insert(InlineKeyboardButton(text=PAGINATION['prev'],
                                           callback_data=ApplicationCB.pagination.new(action="prev", page=page,
                                                                                      offset=offset, limit=limit,
                                                                                      count=count)))
    if count > offset + limit:
        markup.insert(InlineKeyboardButton(text=PAGINATION['next'],
                                           callback_data=ApplicationCB.pagination.new(action="next", page=page,
                                                                                      offset=offset, limit=limit,
                                                                                      count=count)))
    return markup


def inline_choose_region(self, region):
    pass


def apps_inline_button(app_list, count, offset, limit, page):
    markup = pagination_inline_button(count, offset, limit, page)
    max_limit = offset + limit if offset + limit <= count else count
    markup.row(InlineKeyboardButton(text='Фильтрация', callback_data=ApplicationCB.app_action.new(action='filter',
                                                                                                  value='apps')),
               InlineKeyboardButton(text='Сортировка', callback_data=ApplicationCB.app_action.new(action='sort',
                                                                                                  value='apps')))
    markup.row(InlineKeyboardButton(text='Выбрать', callback_data=ApplicationCB.app_action.new(action='select',
                                                                                               value='apps')))
    return markup


def app_select_inline_button(app_list, selected_list, count, offset, limit, page):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton(text='🔙Назад',
                                    callback_data=ApplicationCB.app_action.new(action='back',
                                                                               value='apps')),
               InlineKeyboardButton(text='Продолжить🔜',
                                    callback_data=ApplicationCB.app_action.new(action='continue',
                                                                               value='apps'))
               )
    max_limit = offset + limit if offset + limit <= count else count

    for app in app_list[offset:max_limit]:
        if app.application_id in selected_list:
            markup.insert(InlineKeyboardButton(text=f"☑️{app.application_id}",
                                               callback_data=ApplicationCB.app_action.new(action='choose',
                                                                                          value=app.application_id)))
        else:
            markup.insert(InlineKeyboardButton(text=app.application_id,
                                               callback_data=ApplicationCB.app_action.new(action='choose',
                                                                                          value=app.application_id)))
    if offset > 0:
        markup.insert(InlineKeyboardButton(text=PAGINATION['prev'],
                                           callback_data=ApplicationCB.pagination.new(action="prev", page=page,
                                                                                      offset=offset, limit=limit,
                                                                                      count=count)))
    if count > offset + limit:
        markup.insert(InlineKeyboardButton(text=PAGINATION['next'],
                                           callback_data=ApplicationCB.pagination.new(action="next", page=page,
                                                                                      offset=offset, limit=limit,
                                                                                      count=count)))

    return markup


def region_list_inline(region_list):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton(text='🔙Назад',
                                    callback_data=ApplicationCB.app_action.new(action='back',
                                                                               value='apps')))
    for region in region_list:
        markup.add(InlineKeyboardButton(text=region,
                                        callback_data=ApplicationCB.app_action.new(action="region_choose",
                                                                                   value=region)))
    return markup


def district_list_inline(district_list, selected_district_list):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton(text='🔙Назад',
                                    callback_data=ApplicationCB.app_action.new(action='back',
                                                                               value='region')),
               InlineKeyboardButton(text='Продолжить🔜',
                                    callback_data=ApplicationCB.app_action.new(action='continue',
                                                                               value='district'))
               )
    for district in district_list:
        if district.id in selected_district_list:
            markup.insert(InlineKeyboardButton(text=f"☑️{district.name_uz}",
                                               callback_data=ApplicationCB.app_action.new(action="district_choose",
                                                                                          value=district.id)))
        else:
            markup.insert(InlineKeyboardButton(text=district.name_uz,
                                               callback_data=ApplicationCB.app_action.new(action="district_choose",
                                                                                          value=district.id)))

    return markup
