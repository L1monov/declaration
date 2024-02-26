from aiogram.fsm.state import StatesGroup, State


class Declaration(StatesGroup):
    about = State()
    weight = State()
    dimensions = State()
    shipping_address = State()
    receiving_address = State()
    payment_method = State()