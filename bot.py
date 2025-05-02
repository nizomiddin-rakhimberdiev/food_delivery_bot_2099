from aiogram import Bot, Dispatcher, types, F
import asyncio
from database import Database
from aiogram.fsm.context import FSMContext
from states import RegisterState
from default_keyboards import phone_btn, menu_keyboard, admin_keyboard

bot = Bot(token='7389508313:AAFFWy56tpVt0GpnD5YzI0pVgyNN-P2rLyg')
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


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot is running...")
    asyncio.run(main())