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

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 add prod"), KeyboardButton(text="🛍 orders")],
        [KeyboardButton(text="⚙️ edit prod"), KeyboardButton(text="🛍 get prod")],
        [KeyboardButton(text="👤 add admins"), KeyboardButton(text="📦 curers")],
        [KeyboardButton(text="👤 admins"), KeyboardButton(text="🪙Finance")],
        [KeyboardButton(text="🔙 Orqaga")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)