from aiogram.types import Update
from exceptions.user_exceptions import TooLargeText
from loader import dp


@dp.errors_handler()
async def error_handler(update, exception):
    if isinstance(exception, TooLargeText):
        await Update.get_current().message.answer("255 ta belgidan oshmasin")
        return True

    if isinstance(exception, Exception):
        await Update.get_current().message.answer("Qanaqadir server xatoligi")
        return True
