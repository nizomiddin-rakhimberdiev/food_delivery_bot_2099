from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database

db = Database()


def get_categories_btn():
    categories = db.get_categories()
    print(categories)

    if categories:
        builder = InlineKeyboardBuilder()
        for category in categories:
            builder.button(
                text=category[1],
                callback_data=f"category_{category[0]}"
            )
        builder.adjust(2)  # Har bir qatorda 2 ta tugma
        return builder.as_markup()


def get_products_btn(category_id):
    products = db.get_products(category_id)
    print(products)

    if products:
        builder = InlineKeyboardBuilder()
        for product in products:
            builder.button(
                text=product[1],
                callback_data=f"products_{product[0]}"
            )
        builder.adjust(2)  # Har bir qatorda 2 ta tugma
        return builder.as_markup()


def add_to_cart_btn(product_id: int, count: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"minus_count"),
            InlineKeyboardButton(text=str(count), callback_data=f"count_{product_id}"),
            InlineKeyboardButton(text="➕", callback_data=f"plus_count"),
        ],
        [
            InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"add_to_cart:{product_id}")
        ]
    ])

create_order_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="create_order")
        ]
    ]
)