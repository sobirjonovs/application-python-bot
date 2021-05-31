from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.user import token

fsm = MemoryStorage()
bot: Bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=fsm)
