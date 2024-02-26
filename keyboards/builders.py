from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_builder_reply(text: list| str, max_button_on_row: int = 1, one_time_keyboard: bool = False):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt) for txt in text]

    builder.adjust(max_button_on_row)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)

def create_builder_inline(dict_for_button: dict, max_button_on_row: int = 1):
    # Example dict
    # dict_example = {
    #         'text': 'callback',
    #         'Все пользователи': 'list_users'
    # }
    builder = InlineKeyboardBuilder()

    [builder.button(text=txt, callback_data=callback) for txt, callback in dict_for_button.items()]
    builder.adjust(max_button_on_row)
    return builder.as_markup()