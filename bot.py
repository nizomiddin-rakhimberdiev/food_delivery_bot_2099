from aiogram import Bot, Dispatcher, types, F
import asyncio
from database import Database
from aiogram.fsm.context import FSMContext
from states import RegisterState, AddCategoryState
from default_keyboards import phone_btn, menu_keyboard, admin_keyboard
from inline_keyboards import get_categories_btn

bot = Bot(token='6910861045:AAHv4cNziEbEa-VkgvJRmr3Qr59JNzXfjAQ')
dp = Dispatcher()
db = Database()

SUPER_ADMIN_ID = 726130790

@dp.message(F.text=='/start')
async def start(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    if user_id == SUPER_ADMIN_ID or db.check_admin(user_id):
        await message.answer("Bos nima gap? xoxlagan ishingni qil", reply_markup=admin_keyboard)
    else:
        user = db.check_user(user_id)
        if user:
            await message.answer('Hello, Welcome to delivery bot!', reply_markup=menu_keyboard)
        else:
            await message.answer("Iltimos ro'yxatdan o'tish uchun telefon raqamingizni kiriting: ", reply_markup=phone_btn)
            await state.set_state(RegisterState.phone)

@dp.message(RegisterState.phone)
async def register_handler(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    db.add_user(user_id, phone)
    await state.clear()
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz, Tabriklaymiz", reply_markup=menu_keyboard)

@dp.message(F.text == '📋 add category')
async def add_category(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == SUPER_ADMIN_ID or db.check_admin(user_id):
        await message.answer("Iltimos kategoriya nomini kiriting: ")
        await state.set_state(AddCategoryState.name)
    else:
        await message.answer("Sizda buni qilish huquqi yo'q")

@dp.message(AddCategoryState.name)
async def category_name_handler(message: types.Message, state: FSMContext):
    category_name = message.text
    db.add_category(category_name)
    await state.clear()
    await message.answer("Kategoriya muvaffaqiyatli qo'shildi!", reply_markup=admin_keyboard)

@dp.message(F.text == '🛍 categories')
async def categories_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id == SUPER_ADMIN_ID or db.check_admin(user_id):
        categories = db.get_categories()
        if categories:
            await message.answer("Kategoriyalar:", reply_markup=get_categories_btn())
        else:
            await message.answer("Hozirda hech qanday kategoriya mavjud emas.")
    else:
        await message.answer("Sizda buni qilish huquqi yo'q")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot is running...")
    asyncio.run(main())