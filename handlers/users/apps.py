from aiogram.dispatcher import FSMContext
# from aiogram_dialog import Dialog, DialogManager
from keyboards.inline.callback_builder import ApplicationCB
from loader import dp, bot
from utils.db_api.crud import get_user
from utils.db_api.models import Users, Application as App
from keyboards.default.user import contact
from keyboards.inline.user import inline_user_keyboard, close_inline_user_keyboard, inline_end_keyboard, \
    inline_approve_in_group_keyboard
from sqlalchemy import or_, and_
# from texts.user_text import REGISTRATION as TXT
from states.user import Registration, ProcessApp
from api.service import *
from data import config
import io
import datetime
import textwrap


@dp.message_handler(commands='start', state='*')
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
        pass
    else:
        await bot.send_message("У вас нет доступа")

# TODO: получить список заявок пользователей на доставку.
