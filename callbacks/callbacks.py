from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from data import database
from keyboards import builders
from data.database import My_Database


router = Router()

@router.callback_query()
async def handle_callback(call: CallbackQuery):
    db = My_Database()

    if call.data == 'set_role_manager' or call.data == 'set_role_client':
        tg_id = call.from_user.id
        nickname = call.from_user.username
        role = call.data.split('_')[-1]
        db.insert_one_user(tg_id=tg_id, nickname=nickname, role=role)
        if role == 'manager':
            msg = f'''Супер, Вы - менеджер'''
            await call.message.edit_text(text=msg)
        if role == 'client':
            reply = builders.create_builder_reply(text='📑Начать заполнение дикларации', one_time_keyboard=True)
            msg = '''Супер, Вы - клиент. Давайте перейдем к заполнению накладной\nЕсли нужно вызвать менеджера -> /call_manager'''
            await call.message.edit_text(text=msg)
            await call.message.answer('Чтобы начать заполнение, нажми на кнопку', reply_markup=reply)

