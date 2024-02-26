import asyncio

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import Command
from keyboards import builders
from data.database import My_Database

router = Router()
db = My_Database()

@router.message(Command(commands=["start"]))
async def start(message: Message, bot: Bot):
    msg = """Привет, данный бот создан для тестового задания.\nДля начала давай определимся кто ты)\nPS\nтут можно сделать reply кнопки, но мне кажется так лучше выглядит"""
    reply = builders.create_builder_inline(dict_for_button={
        '🤵Клиент': 'set_role_client',
        '👨🏻‍💼Менеджер': 'set_role_manager'
    }, max_button_on_row=2)

    await message.answer(msg, reply_markup=reply)


@router.message(Command(commands=["call_manager"]))
async def start(message: Message, bot: Bot):
    info_user = db.get_info_user(message.from_user.id)
    if info_user['in_chat']:
        await message.answer('Вы уже в чате')
    if info_user['role'] == 'manager':
        await message.answer('Вы менеджер, кого вам искать ? ))')
    else:
        msg = """Сейчас найду тебе менеджера...."""
        await message.answer(msg)
        free_manager = db.get_free_manager(message.from_user.id)
        if free_manager:
            await message.answer(f'Нашел тебе менеджера\n{free_manager["nickname_tg"]}')
        else:
            await message.answer(f'Не нашёл менеджера((')


@router.message(Command(commands=['leave_chat']))
async def leave_chat(message: Message, bot: Bot):
    info_user = db.get_info_user(message.from_user.id)
    if info_user['in_chat']:
        db.leave_chat(message.from_user.id)
        await message.answer('Вы вышли из чата')
        await bot.send_message(chat_id=info_user['in_chat'], text='Чат завершён')
    else:
        await message.answer('Вы не в чате')

