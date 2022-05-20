from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ContentTypes

from aiogram.dispatcher import FSMContext
# from aiogram_dialog import Dialog, DialogManager
from loader import dp, bot
from utils.db_api.crud import get_user
from utils.db_api.models import Users, Application as App
from keyboards.default.user import contact
from keyboards.inline.user import inline_user_keyboard, close_inline_user_keyboard, inline_end_keyboard
from sqlalchemy import or_, and_
# from texts.user_text import REGISTRATION as TXT
from states.user import Registration, ProcessApp
from api.service import *
import io
import datetime
import textwrap


# from keyboards.constants import LANGUAGES, NAVIGATION


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await get_user()
    print(user)
    print(user.contact)
    print(await state.get_state())
    deep_link = message.get_args()
    if not user:
        await Registration.contact.set()
        if deep_link:
            await state.update_data(deep_link=deep_link)
        await message.answer("Отправить номер телефона в формате 998901234567", reply_markup=contact())
    else:
        if deep_link:
            await state.update_data(deep_link=deep_link)
            resp = await get_application(deep_link)
            if resp and resp.get('data'):
                application = Application(data=resp.get('data'))
                await message.answer(application, reply_markup=inline_user_keyboard(), parse_mode='Markdown')
                await ProcessApp.application.set()
            else:
                await message.answer("Заявка не найдена")


@dp.message_handler(state=Registration.contact, content_types=ContentTypes.CONTACT)
async def contact_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user()
    if user:
        user.contact = message.contact
        await user.update()
    else:
        await Users.create(user_id=message.from_user.id, contact=message.contact.phone_number,
                           username=message.from_user.username,
                           first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    await message.answer("Вы авторизованы", reply_markup=types.ReplyKeyboardRemove())
    if data.get('deep_link'):
        deep_link = data.get('deep_link')
        await state.update_data(deep_link=deep_link)
        resp = await get_application(deep_link)
        if resp and resp.get('data'):
            application = Application(data=resp.get('data'))
            await message.answer(application, reply_markup=inline_user_keyboard(), parse_mode='Markdown')
            await state.finish()
            await ProcessApp.application.set()

        else:
            await message.answer("Заявка не найдена")
            await state.finish()


@dp.message_handler(content_types=ContentTypes.PHOTO, state=[ProcessApp.first_photo, ProcessApp.second_photo])
async def photo_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()
    file = await message.photo[-1].get_file()
    app_id = data.get('deep_link')
    app = await App.query.where(and_(App.app_name == app_id, App.app_finished == False)).gino.first()
    downloaded = await bot.download_file(file['file_path'])

    date = datetime.datetime.now()
    if app:
        if current_state == ProcessApp.first_photo.state:
            await app.update(app_file_first=downloaded.read(), app_updated_date=date).apply()
            if data.get('message_id'):
                try:
                    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=data.get('message_id'),
                                                        reply_markup=None)
                except Exception as e:
                    print(e)
            message = await message.answer("Отправьте второе фото", reply_markup=close_inline_user_keyboard())
            await state.update_data(message_id=message.message_id)
            await ProcessApp.second_photo.set()
        elif current_state == ProcessApp.second_photo.state:
            await app.update(app_file_second=downloaded.read(), app_updated_date=date).apply()
            if data.get('message_id'):
                try:
                    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=data.get('message_id'),
                                                        reply_markup=None)
                except Exception as e:
                    print(e)
            message = await message.answer("Завершите доставку", reply_markup=inline_end_keyboard(),
                                           parse_mode='Markdown')
            await state.update_data(message_id=message.message_id)
            await ProcessApp.confirm.set()
    else:
        await App.create(app_name=app_id, app_owner=message.from_user.id, app_file_first=downloaded.read(),
                         app_status='200', app_created_date=date, app_updated_date=date)
        if data.get('message_id'):
            await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=data.get('message_id'),
                                                reply_markup=None)

        message = await message.answer("Отправьте второе фото", reply_markup=close_inline_user_keyboard())
        await state.update_data(message_id=message.message_id)
        await ProcessApp.second_photo.set()


@dp.callback_query_handler(lambda call: call.data == 'close', state='*')
async def close_handler(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await call.message.edit_text("Заявка закрыта")
    # await call.message.edit_reply_markup(reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'next', state=[ProcessApp.application, ProcessApp.confirm])
async def next_handler(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    if current_state == ProcessApp.application.state:
        message = await call.message.edit_text("Отправьте первую фотку", reply_markup=close_inline_user_keyboard())
        await state.update_data(message_id=message.message_id)
        await ProcessApp.first_photo.set()
    elif current_state == ProcessApp.confirm.state:
        app = await App.query.where(and_(App.app_name == data.get('deep_link'), App.app_finished == False)).gino.first()
        resp = await update_application(app_id=data.get('deep_link'), app_file_first=io.BytesIO(app.app_file_first),
                                        app_file_second=io.BytesIO(app.app_file_second), app_name=app.app_name)
        if resp.get('data'):
            await call.message.edit_text("*Заявка успешно завершена!*", reply_markup=None, parse_mode='Markdown')
        else:
            await call.message.edit_text(resp.get('errorMessage'), reply_markup=None)
        await state.finish()
