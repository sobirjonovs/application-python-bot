import traceback
from types import TracebackType

from aiogram.types import Update
from exceptions.user_exceptions import TooLargeText
from loader import dp


@dp.errors_handler()
async def error_handler(update, exception):
    if isinstance(exception, TooLargeText):
        await Update.get_current().message.answer("255 ta belgidan oshmasin")
        return True

    if isinstance(exception, Exception):
        print(exception.with_traceback(exception.__traceback__), traceback.format_exc())
        await Update.get_current().message.answer("Qanaqadir server xatoligi")
        return True
