from aiogram import Bot, Dispatcher, types, F
import asyncio
from database import Database

bot = Bot(token='7389508313:AAEmVvDmFfpcijZCXMt7brMRnNHLQnWhd9g')
dp = Dispatcher()
db = Database()

@dp.message(F.text=='/start')
async def start(message: types.Message):
    user_id = message.from_user.id
    user = db.check_user(user_id)
    if user:
        await message.answer('Hello, I am a bot!')
    else:
        pass


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot is running...")
    asyncio.run(main())