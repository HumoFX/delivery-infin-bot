import asyncio
import os
import sys

from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.db_api.database import create_db
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    # await set_default_commands(dispatcher)
    await create_db()

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)


if __name__ == '__main__':
    if (sys.platform.startswith('win')
            and sys.version_info[0] == 3
            and sys.version_info[1] >= 8):
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
    executor.start_polling(dp, on_startup=on_startup)

