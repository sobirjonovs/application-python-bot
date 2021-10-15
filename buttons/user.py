from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# PHONE SHARING BUTTON
phone_share_button = ReplyKeyboardMarkup(resize_keyboard=True)
phone_share_button.add(
    KeyboardButton(request_contact=True, text="Telefon ulashish")
)

# REGISTER BUTTON
register_button = ReplyKeyboardMarkup(resize_keyboard=True)
register_button.add(
    KeyboardButton(text="Yo'nalishlar")
)

# REMOVES THE REST KEYBOARD
no_keyboard = ReplyKeyboardRemove()
