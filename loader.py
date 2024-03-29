from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, proxy=config.HTTP_PROXY)
storage = RedisStorage2('localhost', 6379, db=2)
dp = Dispatcher(bot, storage=storage)
