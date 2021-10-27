import re
from pathlib import Path

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from api import get_categories, store_result, check_participant, get_child_categories, get_regions, get_file
from buttons.user import phone_share_button, no_keyboard, register_button
from exceptions.user_exceptions import TooLargeText
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def start(message, state):
    await state.finish()
    nick_name = message.chat.first_name
    text = f"""www.ziyo-tanlovi.uz sayti yurtimizda qator sohalarda faoliyat yurtayotgan iqtidor egalarini aniqlash, ularni yuqori natijalarni qo‘lga kiritishi, yangi tashabbuslar bilan chiqishi, o‘z salohiyatlarini namoyon qilish maqsadida o‘tkazilayotgan tanlovlarni o‘zida mujassam etgan. Ush bot orqali tanlovlarda ishtirok etishingiz mumkin."""
    await message.answer(text, reply_markup=register_button)


@dp.message_handler(text="Tanlov yo'nalishlari")
async def sections(message, state):
    text = "Iltimos, kerakli tanlov yo'nalishini tanlang."
    categories = get_categories()
    sections = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button = []
    parents = {}
    for index, category in enumerate(categories):
        parents[category['name']] = category['id']
        button.append(KeyboardButton(text=category['name']))

    sections.add(*button)

    await state.update_data(parents)

    await state.set_state('select_parent')

    await message.answer(text, reply_markup=sections)


@dp.message_handler(state="select_parent")
async def select_parent(message, state):
    text = "Iltimos, kerakli bo'limni tanlang."
    data = await state.get_data()
    try:
        parent_id = data[message.text]
        await state.update_data({
            "parent_id": parent_id
        })
        children = get_child_categories(parent_id)

        if not children:
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

            return await message.answer(text=re.sub(r'<p>|</p>', '', category['description']),
                                        reply_markup=inline_button)

        sections = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        button = []
        for index, category in enumerate(children):
            button.append(KeyboardButton(text=category['name']))

        sections.add(*button)

        await state.set_state('select_section')

        await message.answer(text, reply_markup=sections)
    except:
        pass


@dp.message_handler(state="select_section")
async def selection(message, state):
    data = await state.get_data()
    try:
        category = next(
            filter(lambda category: message.text in category['name'], get_child_categories(data['parent_id']))
        )
    except:
        pass

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
        return await message.answer("Bu tanlovdan ro'yxatdan o'tgansiz!", reply_markup=register_button)

    try:
        url = get_file()
        await message.reply_document(document=url,
                                     caption="<b>Qo'llanma</b>\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud ")
    except Exception:
        myFile = Path('/')
        path = myFile / 'Tanlov anketasi.doc'
        url = open(path.name, 'rb')
        await message.reply_document(document=url,
                                     caption="<b>Qo'llanma</b>\n\nTanlovda qatnashish uchun siz: \n1. Ism-sharifingiz;\n2. Yashash joyingiz;\n3. Telefon raqamingiz;\n4. Yuqoridagi anketani to'ldirib, PDF formatda tashlashingiz kerak bo'ladi.")

    await state.set_state("full_name")
    await message.answer("Iltimos, to'liq ism-sharifingizni kiriting", reply_markup=no_keyboard)


@dp.message_handler(state="phone", content_types=types.ContentType.CONTACT)
async def send_phone(message, state):
    phone = message.contact.phone_number
    await state.update_data({
        'phone': phone
    })
    await state.set_state("file_upload")
    await message.answer("Iltimos, ijodiy ishingiz va to‘ldirgan anketangizni PDF fayl ko‘rinishida yuboring.(5MB dan oshmasin)", reply_markup=no_keyboard)


@dp.callback_query_handler(text="i_confirm", state="*")
async def upload_file(callback, state):
    await callback.answer()
    message = callback.message
    store_result(await state.get_data())

    await message.answer("Saqlandi", reply_markup=register_button)
    await state.finish()


@dp.callback_query_handler(state="select_region")
async def confirm(callback: types.CallbackQuery, state):
    await callback.answer()
    message = callback.message
    region_name = next(
        filter(lambda region: int(callback.data) == region['id'], get_regions())
    )

    await state.update_data({
        "region": region_name['name'],
        "region_id": region_name['id']
    })

    await state.set_state("phone")
    await message.answer("Iltimos, telefon raqamingizni ulashing", reply_markup=phone_share_button)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state="file_upload")
async def confirm_button(message: types.Message, state):
    file = await message.document.get_file()
    file_url = await file.get_url()

    if file.file_size // 8000 > 625:
        return await message.answer("Faylning o'lchami 5 MB dan katta bo'lmasin!")

    data = await state.get_data()

    if not re.match("[a-zA-Z. -_/:0-9]+\.pdf$", file_url, re.IGNORECASE):
        return await message.answer(text="Iltimos, PDF fayl yuboring.")

    data = {
        "file": file_url,
        "fullname": data['name'],
        "phone": data['phone'],
        "sector_id": data['sector_id'],
        "section": data['section'],
        "region_id": data['region_id'],
        "chat_id": message.chat.id
    }

    await state.update_data(data)

    data = await state.get_data()

    text = """
Ism-sharif: {fullname}
Kategoriya: {section}
Telefon: {phone}
Viloyat/Tuman: {region}

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

    regions = get_regions()

    sections = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    button = []
    for index, region in enumerate(regions):
        button.append(InlineKeyboardButton(text=region['name'], callback_data=region['id']))

    sections.add(*button)

    await state.set_state('select_region')

    await message.answer(text="Iltimos, kerakli viloyatni tanlang", reply_markup=sections)


@dp.message_handler(state="*", commands=['cancel'])
async def cancel_button(message, state):
    await state.finish()
    await start(message, state)


@dp.message_handler(text="Bosh sahifaga", state="*")
async def back_button(message, state):
    await start(message, state)
