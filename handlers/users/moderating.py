import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ContentTypes

from aiogram.dispatcher import FSMContext
# from aiogram_dialog import Dialog, DialogManager
from keyboards.inline.callback_builder import ApplicationCB
from loader import dp, bot
from utils.db_api.crud import get_user
from utils.db_api.models import Users, Application as App
from keyboards.default.user import contact
from keyboards.inline.user import inline_user_keyboard, close_inline_user_keyboard, inline_end_keyboard, \
    inline_approve_in_group_keyboard, inline_approve_confirm_in_group_keyboard
from sqlalchemy import or_, and_
# from texts.user_text import REGISTRATION as TXT
from states.user import Registration, ProcessApp
from api.service import *
from data import config
import io
import datetime
import textwrap

CONSTANTS = {
    "approve": "✅",
    "reject": "❌",
}
ACTION_CONSTANTS = {
    "approve": "подтвердить",
    "reject": "отклонить",
}


class TimeDelta(datetime.timedelta):
    def __str__(self):
        _times = super(TimeDelta, self).__str__().split(':')
        _times = [int(i) for i in _times]
        _times = [str(i) for i in _times]
        if "," in _times[0]:
            _hour = int(_times[0].split(',')[-1].strip())
            if _hour:
                _times[0] += " часов" if _hour > 1 else " час"
            else:
                _times[0] = _times[0].split(',')[0]
        else:
            _hour = int(_times[0].strip())
            if _hour:
                _times[0] += " часов" if _hour > 1 else " часов"
            else:
                _times[0] = ""
        _min = int(_times[1])
        if _min:
            _times[1] += " минут" if _min > 1 else " минуту"
        else:
            _times[1] = ""
        _sec = int(_times[2])
        if _sec:
            _times[2] += " секунд" if _sec > 1 else " секунд"
        else:
            _times[2] = ""
        return ", ".join([i for i in _times if i]).strip(" ,").title()


@dp.callback_query_handler(ApplicationCB.in_group.filter(), state='*')
async def moderation_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data.get('act')
    value = callback_data.get('val')
    app_name = callback_data.get('app_id')
    msg = callback_data.get('msg')
    resp_text = ""
    app = await App.query.where(
        and_(App.app_name == app_name, App.app_finished == False)).gino.first()
    conf_action = True if action == "approve" else False
    await call.message.edit_text(text=f"Вы уверены, что хотите *{ACTION_CONSTANTS[action]}* фотографии данной заявки?",
                                 reply_markup=inline_approve_confirm_in_group_keyboard(value, app_name, msg, conf_action),
                                 parse_mode="Markdown")


@dp.callback_query_handler(ApplicationCB.in_group_confirmation.filter(), state='*')
async def moderation_confirmation_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data.get('act')
    value = callback_data.get('val')
    app_name = callback_data.get('app_id')
    msg = callback_data.get('msg')
    resp_text = ""
    app = await App.query.where(
        and_(App.app_name == app_name, App.app_finished == False)).gino.first()
    if action == 'back':
        await call.message.edit_text(text="Подтвердите фото",
                                     reply_markup=inline_approve_in_group_keyboard(value, app_name, msg),
                                     parse_mode="Markdown")
    else:
        if action == 'approve':
            resp = await update_application(app_id=value,
                                            app_file_first=io.BytesIO(app.app_file_first),
                                            app_file_second=io.BytesIO(app.app_file_second), app_name=app.app_name)
            if resp.get('data'):
                apps = await MyApp.query.where(and_(MyApp.app_id == value, MyApp.finished == False)).gino.all()
                for app in apps:
                    await app.update(finished=True).apply()

                resp_text = "*💠Заявка успешно завершена!*"
            elif resp.get('errorMessage'):
                resp_text = f"*🚫Ошибка при завершении заявки:* {resp.get('errorMessage')}"
        elif action == 'reject':
            resp_text = "*🚫Заявка отклонена!* Пожалуйста, проверьте качество фотографий и повторите попытку."

        await app.update(check_end_date=datetime.datetime.now()).apply()
        diff: datetime.timedelta = app.check_end_date - app.check_start_date
        await call.message.delete()
        await bot.delete_message(config.ADMIN_GROUP, int(msg))
        await bot.delete_message(config.ADMIN_GROUP, int(msg) + 1)
        text = f"🆔 {app.app_name} {CONSTANTS[action]}\n"
        text += f"📦 #id{app.app_owner}\n"
        text += f"🛂 #id{call.from_user.id} за {TimeDelta(seconds=int(diff.total_seconds()))}\n"
        if resp_text:
            text += f"{resp_text}\n"
        await bot.send_message(config.ADMIN_GROUP, text, parse_mode="Markdown")
        deliver_text = f"🆔 {app.app_name} {CONSTANTS[action]}\n {resp_text}"
        await bot.send_message(app.app_owner, deliver_text, parse_mode="Markdown")
