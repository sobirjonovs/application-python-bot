from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from buttons.user import phone_share_button, sections, no_keyboard
from exceptions.user_exceptions import TooLargeText
from loader import dp, bot
from queries import db


@dp.message_handler(CommandStart())
async def start(message, state):
    isExist = db.select(table="reviews", what="chat_id", condition={'chat_id': message.chat.id}, one=True)

    if isExist is not None:
        return await message.answer("Assalomu alaykum!")

    nick_name = message.chat.first_name
    text = f"""
    Assalomu alaykum, hurmatli  {nick_name}! 
    
Iltimos telefon raqamingizni ulashing!
    """
    await state.set_state("phone")
    await message.answer(text, reply_markup=phone_share_button)


@dp.message_handler(state="phone", content_types=types.ContentType.CONTACT)
async def send_phone(message, state):
    phone = message.contact.phone_number
    await state.update_data({
        'phone': phone
    })
    await state.set_state("full_name")
    await message.answer("Iltimos to'liq ism sharifingizni kiriting", reply_markup=no_keyboard)


@dp.message_handler(state="full_name")
async def send_full_name(message, state):
    full_name = message.text

    if len(full_name) > 255:
        raise TooLargeText

    await state.update_data({
        'name': full_name
    })

    await state.set_state("sections")
    await message.answer("Iltimos bo'limni tanlang", reply_markup=sections)


@dp.message_handler(state="sections")
async def send_sections(message, state):
    section = message.text
    data = await state.get_data()

    try:
        columns = {
            'chat_id': message.chat.id,
            'name': data['name'],
            'phone': data['phone'],
            'section': section
        }
        db.insert(
            table="reviews",
            columns=columns.keys(),
            values=columns.values()
        )
    except Exception as e:
        raise Exception

    await message.answer("Saqlandi", reply_markup=no_keyboard)
    await state.finish()
