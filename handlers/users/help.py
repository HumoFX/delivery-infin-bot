from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Command

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = """Инструкция по использованию бота:\n
    Сканируйте qr код, который направит вас на этот бот.\n
    Нажмите на /start для начала работы.\n
    Если qr валидный, то получите информацию о заявке.\n
    """

    await message.answer("\n".join(text))


@dp.message_handler(Command("scan"))
async def bot_qr_scan(message: types.Message):
    text = "Отправьте фото с QR-кодом для проверки подлинности"
    await message.answer(text=text)
