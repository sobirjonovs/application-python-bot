from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# PHONE SHARING BUTTON
phone_share_button = ReplyKeyboardMarkup(resize_keyboard=True)
phone_share_button.add(
    KeyboardButton(request_contact=True, text="Telefonni ulashish")
)

# REGISTER BUTTON
register_button = ReplyKeyboardMarkup(resize_keyboard=True)
register_button.add(
    KeyboardButton(text="Tanlov yo'nalishlari")
)

# REMOVES THE REST KEYBOARD
no_keyboard = ReplyKeyboardRemove()
