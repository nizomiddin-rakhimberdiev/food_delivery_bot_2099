from aiogram import Bot, Dispatcher, types, F
import asyncio
from database import Database
from aiogram.fsm.context import FSMContext
from states import RegisterState, AddCategoryState, AddProductState, GetProductState
from default_keyboards import phone_btn, menu_keyboard, admin_keyboard
from inline_keyboards import get_categories_btn, get_products_btn

bot = Bot(token='6910861045:AAHv4cNziEbEa-VkgvJRmr3Qr59JNzXfjAQ')

dp = Dispatcher()
db = Database()

SUPER_ADMIN_ID = 726130790


@dp.message(F.text == '/start')
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.check_user(user_id)
    if user:
        await message.answer('Hello, Welcome to delivery bot!', reply_markup=menu_keyboard)
    else:
        await message.answer("Iltimos ro'yxatdan o'tish uchun telefon raqamingizni kiriting: ", reply_markup=phone_btn)
        await state.set_state(RegisterState.phone)


@dp.message(F.text=='/admin')
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == SUPER_ADMIN_ID or db.check_admin(user_id):
        await message.answer("Bos nima gap? xoxlagan ishingni qil", reply_markup=admin_keyboard)
    else:
        return

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


@dp.message(F.text == '📋 add prod')
async def add_product_handler(message: types.Message, state: FSMContext):
    await message.answer("Maxsulot nomini kiriting: ")
    await state.set_state(AddProductState.name)


@dp.message(AddProductState.name)
async def product_name_handler(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(name=product_name)
    await message.answer("Maxsulot haqida to'liq ma'lumot kiriting: ")
    await state.set_state(AddProductState.description)


@dp.message(AddProductState.description)
async def product_description_handler(message: types.Message, state: FSMContext):
    product_description = message.text
    await state.update_data(description=product_description)
    await message.answer("Maxsulot narxini kiriting: ")
    await state.set_state(AddProductState.price)


@dp.message(AddProductState.price)
async def product_price_handler(message: types.Message, state: FSMContext):
    product_price = message.text
    await state.update_data(price=product_price)
    await message.answer("Maxsulot rasmini yuboring: ")
    await state.set_state(AddProductState.image)


@dp.message(AddProductState.image)
async def product_photo_handler(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(image=photo)
    await message.answer("Maxsulot kategoriyasini tanlng: ", reply_markup=get_categories_btn())
    await state.set_state(AddProductState.category)


@dp.callback_query(AddProductState.category, F.data.startswith('category'))
async def product_category_handler(callback_query: types.CallbackQuery, state: FSMContext):
    category_id = callback_query.data.split('_')[1]
    data = await state.get_data()
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    db.add_product(name, description, price, image, category_id)
    await callback_query.message.answer("Maxsulot qo'shildi")
    await state.clear()


@dp.message(F.text == '📋 Menu')
async def menu_handler(message: types.Message, state: FSMContext):
    await message.answer("Kategoriyalardan birini tanlang", reply_markup=get_categories_btn())
    await state.set_state(GetProductState.category)


@dp.callback_query(GetProductState.category, F.data.startswith('category'))
async def category_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    category_id = callback_query.data.split('_')[1]
    message_id = callback_query.message.message_id
    products = db.get_product(category_id)
    if products:
        await callback_query.message.edit_text("Maxsulotlardan birini tanlang", reply_markup=get_products_btn(category_id))
        await state.set_state(GetProductState.product)
    else:
        await callback_query.answer("Bu kategoriya bo'yicha maxsulotlar mavjud emas.")
        # await state.set_state(GetProductState.category)


@dp.callback_query(GetProductState.product, F.data.startswith('products'))
async def product_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]
    product = db.get_product(product_id)
    image = product[5]
    name = product[1]
    description = product[2]
    price = product[3]
    status = product[4]
    text = f"{name}\n\n{description}\n\nNarxi: {price} so'm"
    await callback_query.message.answer_photo(photo=image, caption=text)
    await state.clear()




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Bot is running...")
    asyncio.run(main())
