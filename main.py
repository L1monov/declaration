from aiogram import Bot, Dispatcher, Router, F
import asyncio
from config import TOKEN_BOT
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.filters import Command
from handlers import user_commands, fill_declaration, bot_message
from data.database import My_Database
from callbacks import callbacks

router = Router()





async def main():
    bot = Bot(token=TOKEN_BOT)

    dp = Dispatcher()

    dp.include_routers(
        router,
        user_commands.router,
        fill_declaration.router,
        callbacks.router,
        bot_message.router

    )

    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot rolling')
    await dp.start_polling(bot)

if __name__ == '__main__':
    db = My_Database()
    db.create_tables() # Создаем таблицы в бд (если их нет)
    asyncio.run(main())