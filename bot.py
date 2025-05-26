from aiogram import Bot, Dispatcher, types, F
import asyncio
from database import Database
from aiogram.fsm.context import FSMContext
from states import RegisterState, AddCategoryState, AddProductState, GetProductState, CreateOrderState, AddAdvertState
from default_keyboards import phone_btn, menu_keyboard, admin_keyboard, location_btn
from inline_keyboards import get_categories_btn, get_products_btn, add_to_cart_btn, create_order_button, resend_btn
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="726130790")

bot = Bot(token='6514890915:AAFqppbIr0zur8BjdgvTQuG_3oh86uBXuB8')

dp = Dispatcher()
db = Database()

SUPER_ADMIN_ID = 726130790

from aiogram import Bot
import os


async def download_photo(file_id: str, bot: Bot, save_dir: str = "images") -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split("/")[-1]

    # Saqlash papkasini yaratish
    os.makedirs(save_dir, exist_ok=True)

    destination = os.path.join(save_dir, file_name)

    await bot.download_file(file_path, destination)
    return destination  # Bu path ni bazaga saqlaysiz


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
    file_id = message.photo[-1].file_id
    photo = await download_photo(file_id, bot)
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
    product_id = product[0]
    image_path = product[5]
    image = types.FSInputFile(image_path)
    name = product[1]
    description = product[2]
    price = product[3]
    status = product[4]
    text = f"{name}\n\n{description}\n\nNarxi: {price} so'm"
    await callback_query.message.answer_photo(photo=image, caption=text, reply_markup=add_to_cart_btn(product_id, 1))
    await state.clear()

@dp.callback_query(F.data == 'plus_count')
async def plus_count_handler(callback_query: types.CallbackQuery):
    print("Plus bosildi")
    product_id = callback_query.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]
    print(product_id)
    count = int(callback_query.message.reply_markup.inline_keyboard[0][1].text)
    count += 1
    await callback_query.message.edit_reply_markup(reply_markup=add_to_cart_btn(product_id, count))


@dp.callback_query(F.data == 'minus_count')
async def minus_count_handler(callback_query: types.CallbackQuery):
    print("Minus bosildi")
    product_id = callback_query.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]
    count = int(callback_query.message.reply_markup.inline_keyboard[0][1].text)
    if count > 1:
        count -= 1
        await callback_query.message.edit_reply_markup(reply_markup=add_to_cart_btn(product_id, count))
    else:
        await callback_query.answer("Soni 1 dan kam bo'lishi mumkin emas!")
        
@dp.callback_query(F.data.startswith('add_to_cart'))
async def add_to_cart_handler(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split(":")[1])
    user_id = callback_query.from_user.id
    count = int(callback_query.message.reply_markup.inline_keyboard[0][1].text)
    product = db.get_product(product_id)
    print(product)
    price = product[3]
    db.add_to_cart(product_id, user_id, count, price)
    await callback_query.answer("Maxsulot savatchaga qo'shildi!")

@dp.message(F.text == '🛒 Savatcha')
async def cart_handler(message: types.Message):
    user_id = message.from_user.id
    cart_data = db.get_cart_data(user_id)
    total_price = 15000
    if cart_data:
        text = "Savatchangizdagi maxsulotlar:\n"
        for item in cart_data:
            product = db.get_product(item[2])
            total_price += item[4]
            text += f"{product[1]} - {item[3]} dona. Jami: {item[4]} so'm\n"
        text += f"\nYetkazib berish: 15000 so'm\n\nJami Narxi: {total_price} so'm\n"
        await message.answer(text, reply_markup=create_order_button)
    else:
        await message.answer("Savatchangiz bo'sh.")

@dp.callback_query(F.data == 'create_order')
async def create_order_handler(callback_query: types.CallbackQuery, state: FSMContext):
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=message_id)
    await callback_query.message.answer("Iltimos manzilni yuboring: ", reply_markup=location_btn)
    await state.set_state(CreateOrderState.address)

@dp.message(CreateOrderState.address, F.location)
async def address_handler(message: types.Message, state: FSMContext):
    address_lat = message.location.latitude
    address_lon = message.location.longitude
    print(address_lat, address_lon)
    location = geolocator.reverse((address_lat, address_lon), language='uz')
    print(location.address)
    await state.update_data(address=location.address)
    await message.answer("Iltimos telefon raqamingizni yuboring: ")
    await state.set_state(CreateOrderState.phone)

@dp.message(CreateOrderState.phone)
async def phone_handler(message: types.Message, state: FSMContext):
    phone = message.text
    data = await state.get_data()
    address = data['address']
    db.create_order(message.from_user.id, address, phone)
    await message.answer("Buyurtmangiz qabul qilindi. Tez orada yetkazib beramiz.")
    db.clear_cart(message.from_user.id)
    await state.clear()

@dp.message(F.text == '🛍 add advert')
async def add_advert_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == SUPER_ADMIN_ID or db.check_admin(user_id):
        await message.answer("Iltimos reklama rasmni yuboring: ")
        await state.set_state(AddAdvertState.image)
    else:
        return 
    
@dp.message(AddAdvertState.image, F.photo)
async def advert_image_handler(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(image=file_id)
    await message.answer("Iltimos reklama matnini kiriting: ")
    await state.set_state(AddAdvertState.content)

@dp.message(AddAdvertState.content)
async def advert_content_handler(message: types.Message, state: FSMContext):
    content = message.text
    data = await state.get_data()
    image_file_id = data['image']
    for user in db.get_all_users_user_id():
        try:
            if user == str(SUPER_ADMIN_ID) or db.check_admin(user):
                await bot.send_photo(chat_id=user, photo=image_file_id, caption=content, reply_markup=resend_btn(message_id=message.message_id))
            else:
                await bot.send_photo(chat_id=user, photo=image_file_id, caption=content)
        except Exception as e:
            print(f"Error sending advert to user {user}: {e}")
    await message.answer("Reklama muvaffaqiyatli yuborildi!", reply_markup=admin_keyboard)
    await state.clear()

@dp.callback_query(F.data.startswith('resend_advert'))
async def resend_advert_handler(callback_query: types.CallbackQuery):
    message_id = callback_query.data.split(':')[1]
    user_id = callback_query.from_user.id
    advert_message = await bot.get_message(chat_id=user_id, message_id=message_id)
    if advert_message:
        try:
            for user in db.get_all_users_user_id():
                if user == str(SUPER_ADMIN_ID) or db.check_admin(user):
                    await bot.send_photo(chat_id=user, photo=advert_message.photo[-1].file_id, caption=advert_message.caption, reply_markup=resend_btn(message_id=message_id))
                else:
                    await bot.send_photo(chat_id=user_id, photo=advert_message.photo[-1].file_id, caption=advert_message.caption)
            await callback_query.answer("Reklama qayta yuborildi!")
        except Exception as e:
            await callback_query.answer(f"Reklama yuborishda xatolik: {e}")
    else:
        await callback_query.answer("Reklama topilmadi.")

async def start_bot():
        await bot.send_message(SUPER_ADMIN_ID, text="Bot ishga tushdi")


async def main():
    await start_bot()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Bot is running...")
    asyncio.run(main())
