from aiogram.utils import executor
from handlers import dp, bot, db
from config.user import admins


async def on_startup(dispatcher):
    db.create(table='reviews', id="int AUTO_INCREMENT PRIMARY KEY", name="VARCHAR(255) DEFAULT NULL",
              chat_id="VARCHAR(255)", phone="VARCHAR(255) DEFAULT NULL", section="VARCHAR(255) DEFAULT NULL",
              )
    for admin in admins:
        await bot.send_message(chat_id=admin, text="Bot ishga tushdi")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
