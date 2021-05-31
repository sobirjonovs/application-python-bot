from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# PHONE SHARING BUTTON
phone_share_button = ReplyKeyboardMarkup(resize_keyboard=True)
phone_share_button.add(
    KeyboardButton(request_contact=True, text="Telefon ulashish")
)

# REMOVES THE REST KEYBOARD
no_keyboard = ReplyKeyboardRemove()

# SECTIONS BUTTON
sections = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
sections.add(
    KeyboardButton(text="IT"),
    KeyboardButton(text="IT 1"),
    KeyboardButton(text="IT 2"),
    KeyboardButton(text="IT 3"),
    KeyboardButton(text="IT 4"),
    KeyboardButton(text="IT 5"),
)
