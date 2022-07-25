from aiogram import types
from aiogram.dispatcher import FSMContext
# from aiogram_dialog import Dialog, DialogManager
from keyboards.inline.callback_builder import ApplicationCB
from loader import dp, bot
from utils.db_api.crud import get_user
from utils.db_api.models import Users, Application as App
from keyboards.default.user import contact
from keyboards.inline.user import inline_user_keyboard, close_inline_user_keyboard, inline_end_keyboard, \
    inline_approve_in_group_keyboard, apps_inline_button, app_select_inline_button
from sqlalchemy import or_, and_
# from texts.user_text import REGISTRATION as TXT
from states.user import Registration, ProcessApp
from api.service import *
from data import config
import io
import datetime
import textwrap


@dp.message_handler(commands='app_list', state='*')
async def app_list_handler(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await get_user()
    deep_link = message.get_args()
    if not user:
        await Registration.contact.set()
        if deep_link:
            await state.update_data(deep_link=deep_link)
        await message.answer("Отправить номер телефона в формате 998901234567", reply_markup=contact())
    elif user.is_admin or user.is_courier and user.is_active:
        # get list of applications
        data = await get_application_list()
        app_list = ApplicationList(**data)
        chosen_region = None
        region_list = set()
        district_list = set()
        for app in app_list.data:
            region_list.add(app.region)
            district_list.add(app.district)
        if len(region_list) == 1:
            chosen_region = next(iter(region_list))
        count = len(app_list.data)
        offset = 0
        page = 0
        limit = 8
        await state.update_data({"app_list": data, "offset": offset, "page": page, "limit": limit, "count": count,
                                 "region_list": region_list, "district_list": district_list})

        await message.answer(app_list.__str__(), parse_mode='Markdown', reply_markup=apps_inline_button(app_list.data,
                                                                                                        count,
                                                                                                        offset, limit,
                                                                                                        page))

    else:
        await message.answer("У вас нет доступа")


# TODO: получить список заявок пользователей на доставку.

@dp.callback_query_handler(ApplicationCB.app_action.filter(), state='*')
async def app_action_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    app = data.get('app_list')
    app_list = ApplicationList(**app)
    offset = data.get('offset', 0)
    limit = data.get('limit', 8)
    count = data.get('count', None)
    page = data.get('page', None)
    selected_list = data.get('selected_list', [])
    action = callback_data.get('action')
    chosen_region = data.get('chosen_region', None)
    chosen_district = data.get('chosen_district', None)
    value = callback_data.get('value')
    if action == 'filter':
        if not chosen_region:
            await call.message.edit_text("Выберите регион", parse_mode='Markdown', reply_markup=None)
    elif action == 'sort':
        pass
    elif action == 'select':
        selected_list = []
        await call.message.edit_text(app_list.__str__(), parse_mode='Markdown',
                                     reply_markup=app_select_inline_button(app_list.data,
                                                                           selected_list,
                                                                           count,
                                                                           offset, limit,
                                                                           page))
    elif action == 'back':
        await call.message.edit_text(app_list.__str__(), parse_mode='Markdown',
                                     reply_markup=apps_inline_button(app_list.data,
                                                                     count,
                                                                     offset, limit,
                                                                     page))
    elif action == 'continue':
        pass

    elif action == 'choose':
        if value not in selected_list:
            selected_list.append(value)
        else:
            selected_list.remove(value)
        await state.update_data({"selected_list": selected_list})
        await call.message.edit_text(app_list.__str__(), parse_mode='Markdown',
                                     reply_markup=app_select_inline_button(app_list.data,
                                                                           selected_list,
                                                                           count,
                                                                           offset, limit,
                                                                           page))
