import asyncio

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import Command
from keyboards import builders
from data.database import My_Database

router = Router()
db = My_Database()

@router.message()
async def all_message(message: Message, bot: Bot):

    info_user = db.get_info_user(message.from_user.id)
    if info_user['in_chat']:
        await bot.send_message(chat_id=info_user['in_chat'], text=f'<b>Новое сообщение</b>\n{message.text}\n\nЧтобы покинуть чат -> /leave_chat', parse_mode='HTML')
    else:
        await message.answer('Я вас не понимаю ((')
