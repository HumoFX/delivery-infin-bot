from aiogram import types
from aiogram.dispatcher import FSMContext
# from aiogram_dialog import Dialog, DialogManager
from keyboards.inline.callback_builder import ApplicationCB
from loader import dp, bot
from utils.db_api.crud import get_user
from utils.db_api.models import Users, Application as App, District, Region
from keyboards.default.user import contact
from keyboards.inline.user import inline_user_keyboard, close_inline_user_keyboard, inline_end_keyboard, \
    inline_approve_in_group_keyboard, apps_inline_button, app_select_inline_button, region_list_inline, \
    district_list_inline
from sqlalchemy import or_, and_
# from texts.user_text import REGISTRATION as TXT
from states.user import Registration, ProcessApp
from api.service import *
from data import config
import io
import datetime
import textwrap


def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)


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
                                 "region_list": list(region_list), "district_list": list(district_list)})

        await message.answer(await app_list.new_str(), parse_mode='Markdown', reply_markup=apps_inline_button(app_list.data,
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
    selected_district_list = data.get('selected_district_list', [])
    action = callback_data.get('action')
    region_list = data.get('region_list', [])
    district_list = data.get('district_list', [])
    filtered_apps = data.get('filtered_apps', [])
    chosen_region = data.get('chosen_region', None)
    chosen_district = data.get('chosen_district', None)
    value = callback_data.get('value')
    if action == 'filter':
        if not chosen_region:
            await call.message.edit_text("Выберите регион", parse_mode='Markdown',
                                         reply_markup=region_list_inline(region_list))
    elif action == 'sort':
        pass
    elif action == 'select':
        if not filtered_apps:
            text = f"Результатов {len(filtered_apps)}. Поменяйте настройки фильтрации"
        else:
            data = {"data": filtered_apps}
            app_list = ApplicationList(**data)
            text = await app_list.new_str()
        selected_list = []
        await call.message.edit_text(text, parse_mode='Markdown',
                                     reply_markup=app_select_inline_button(app_list.data,
                                                                           selected_list,
                                                                           count,
                                                                           offset, limit,
                                                                           page))
    elif action == 'back':
        await call.message.edit_text(await app_list.new_str(), parse_mode='Markdown',
                                     reply_markup=apps_inline_button(app_list.data,
                                                                     count,
                                                                     offset, limit,
                                                                     page))
    elif action == 'continue':
        app_result = []
        for app in app_list.data:
            district = await District.query.where(District.name_uz == app.district).gino.first()
            if district.id in selected_district_list:
                app_result.append(app.to_dict())
        data = {"data": app_result}
        await state.update_data({"filtered_apps": app_result})
        if not app_result:
            text = f"Результатов {len(app_result)}. Поменяйте настройки фильтрации"
        else:
            text = await ApplicationList(**data).new_str()
        await call.message.edit_text(text, parse_mode='Markdown',
                                     reply_markup=apps_inline_button(app_result,
                                                                     count,
                                                                     offset, limit,
                                                                     page))

    elif action == 'choose':
        if filtered_apps:
            data = {"data": filtered_apps}
            app_list = ApplicationList(**data)
        if value not in selected_list:
            selected_list.append(value)
        else:
            selected_list.remove(value)
        print("selected_list", selected_list)
        await state.update_data({"selected_list": selected_list})
        await call.message.edit_text(await app_list.new_str(), parse_mode='Markdown',
                                     reply_markup=app_select_inline_button(app_list.data,
                                                                           selected_list,
                                                                           count,
                                                                           offset, limit,
                                                                           page))
    elif action == 'region_choose':
        region = await Region.query.where(Region.name_uz == value).gino.first()
        district_list = await District.query.where(District.region_id == region.id).gino.all()
        await state.update_data({"region_id": region.id})
        app_result = []
        for app in app_list.data:
            if app.region == value:
                app_result.append(app)
        text = f"Выбрано {len(app_result)} заявок.\n Выберите регион"
        await call.message.edit_text(text, parse_mode='Markdown',
                                     reply_markup=district_list_inline(district_list, selected_district_list))

    elif action == 'district_choose':
        if int(value) not in selected_district_list:
            selected_district_list.append(int(value))
        else:
            selected_district_list.remove(int(value))
        region_id = data.get("region_id")
        district_list = await District.query.where(District.region_id == region_id).gino.all()
        await state.update_data({"selected_district_list": selected_district_list})
        app_result = []
        for app in app_list.data:
            district = await District.query.where(District.name_uz == app.district).gino.first()
            if district.id in selected_district_list:
                app_result.append(app)
        text = f"Выбрано {len(app_result)} заявок.\nВыберите район"
        await call.message.edit_text(text, parse_mode='Markdown',
                                     reply_markup=district_list_inline(district_list, selected_district_list))


