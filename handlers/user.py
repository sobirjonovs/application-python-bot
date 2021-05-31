from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from buttons.user import phone_share_button, sections, no_keyboard, register_button
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
    
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas a tempus odio. 
Quisque nec euismod nisi. Integer laoreet vel mauris id tincidunt. 
Phasellus at blandit justo, eget scelerisque ex. Sed placerat velit fringilla, hendrerit est vitae, 
pulvinar nunc. Morbi ut augue pretium ante facilisis laoreet ut pretium purus. Ut hendrerit orci at rutrum feugiat.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas a tempus odio. 
Quisque nec euismod nisi. Integer laoreet vel mauris id tincidunt. 
Phasellus at blandit justo, eget scelerisque ex. Sed placerat velit fringilla, hendrerit est vitae, 
pulvinar nunc. Morbi ut augue pretium ante facilisis laoreet ut pretium purus. Ut hendrerit orci at rutrum feugiat.
"""
    await state.set_state("register")
    await message.answer(text, reply_markup=register_button)


@dp.message_handler(state="register", text="Ro'yxatdan o'tish")
async def register(message, state):
    text = "Ro'yxatdan o'tish uchun kerakli bo'limni tanlang"
    await state.set_state("sections")
    await message.answer(text, reply_markup=sections)


@dp.message_handler(state="sections")
async def select_section(message, state):
    await state.update_data({
        'section': message.text
    })
    text = "Telefon raqamni ulashing"
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

    await state.set_state("save")
    await save(message, state)


@dp.message_handler(state="save")
async def save(message, state):
    data = await state.get_data()

    try:
        columns = {
            'chat_id': message.chat.id,
            'name': data['name'],
            'phone': data['phone'],
            'section': data['section']
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
