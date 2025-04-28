from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamingizni yuboring", request_contact=True),
        ]
    ],
    resize_keyboard=True
)

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Menu"), KeyboardButton(text="🛍 Buyurtmalarim")],
        [KeyboardButton(text="⚙️ Sozlamalar")],
    ],
    resize_keyboard=True
)