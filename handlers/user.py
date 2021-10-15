from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from api import get_categories, store_result, check_participant
from buttons.user import phone_share_button, no_keyboard, register_button
from exceptions.user_exceptions import TooLargeText
from loader import dp, bot
from queries import db
import re


@dp.message_handler(CommandStart(), state="*")
async def start(message, state):
    await state.finish()
    nick_name = message.chat.first_name
    text = f"""
            Assalomu alaykum, hurmatli  {nick_name}!
Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos 
sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam
recusandae alias error harum maxime adipisci amet laborum. Perspiciatis 
minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit 
quibusdam sed amet tempora. 
            """
    await message.answer(text, reply_markup=register_button)


@dp.message_handler(text="Yo'nalishlar")
async def sections(message, state):
    text = "Iltimos, kerakli bo'limni tanlang."
    categories = get_categories()
    sections = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button = []
    for index, category in enumerate(categories):
        button.append(KeyboardButton(text=category['name']))

    sections.add(*button)

    await state.set_state('select_section')

    await message.answer(text, reply_markup=sections)


@dp.message_handler(state="select_section")
async def selection(message, state):
    category = next(
        filter(lambda category: message.text in category['name'], get_categories())
    )

    await state.finish()

    await state.update_data({
        "section": category['name'],
        "sector_id": category['id']
    })

    inline_button = InlineKeyboardMarkup()
    inline_button.add(
        InlineKeyboardButton(text="A'zo bo'lish", callback_data="subscribe")
    )

    await message.answer(text=re.sub(r'<p>|</p>', '', category['description']), reply_markup=inline_button)


@dp.callback_query_handler(text="subscribe")
async def select_section(callback: types.CallbackQuery, state):
    message = callback.message
    await callback.answer()
    data = await state.get_data()

    is_exists = check_participant({
        "chat_id": message.chat.id,
        "sector_id": data['sector_id']
    })

    if is_exists:
        await state.finish()
        return await message.answer("Bundan ro'yxatdan o'tgansiz!", reply_markup=register_button)

    await state.set_state("full_name")
    await message.answer("Iltimos to'liq ism sharifingizni kiriting")


@dp.message_handler(state="phone", content_types=types.ContentType.CONTACT)
async def send_phone(message, state):
    phone = message.contact.phone_number
    await state.update_data({
        'phone': phone
    })
    await state.set_state("file_upload")
    await message.answer("Fayl yuklang", reply_markup=no_keyboard)


@dp.callback_query_handler(text="i_confirm", state="*")
async def upload_file(callback, state):
    await callback.answer()
    message = callback.message
    store_result(await state.get_data())

    await message.answer("Saqlandi", reply_markup=register_button)
    await state.finish()


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state="file_upload")
async def confirm_button(message, state):
    file_url = await message.document.get_url()
    data = await state.get_data()

    if not re.match("[a-zA-Z. -_\/:0-9]+\.pdf$", file_url):
        return await message.answer(text="PDF fayl tashla e!")

    data = {
        "file": file_url,
        "fullname": data['name'],
        "phone": data['phone'],
        "sector_id": data['sector_id'],
        "section": data['section'],
        "chat_id": message.chat.id
    }

    await state.update_data(data)

    text = """
Ism: {fullname}
Kategoriya: {section}
Telefon: {phone}

<b>Ma'lumotlar to'g'riligini tasdiqlaysizmi?</b>
""".format(**data)

    confirm_button = InlineKeyboardMarkup(row_width=2)
    confirm_button.row(
        InlineKeyboardButton(text="Tasdiqlayman", callback_data="i_confirm"),
        InlineKeyboardButton(text="Bekor qilish", callback_data="i_cancel"),
    )

    await message.answer(text=text, reply_markup=confirm_button)


@dp.callback_query_handler(text="i_cancel", state="*")
async def cancel_i(callback: types.CallbackQuery, state):
    await callback.answer()
    await state.finish()
    await callback.message.answer(text="Yo'nalishlardan birini tanla", reply_markup=register_button)


@dp.message_handler(state="full_name")
async def send_full_name(message, state):
    full_name = message.text

    if len(full_name) > 255:
        raise TooLargeText

    await state.update_data({
        'name': full_name
    })

    await state.set_state("phone")
    await message.answer("Iltimos telefon raqamingizni ulashing", reply_markup=phone_share_button)


@dp.message_handler(state="*", commands=['cancel'])
async def cancel_button(message, state):
    await state.finish()
    await start(message, state)


@dp.message_handler(text="Bosh sahifaga", state="*")
async def back_button(message, state):
    await start(message, state)
