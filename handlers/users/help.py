from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Command

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))


@dp.message_handler(Command("scan"))
async def bot_qr_scan(message: types.Message):
    text = "Отправьте фото с QR-кодом для проверки подлинности"
    await message.answer(text=text)
