import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InputFile

from utils.states import Declaration
from keyboards import builders
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas




def create_pdf(file_path, text):
    text_for_write = f"""Описание {text['about']}
    Вес груза {text['weight']}
    Габариты груза {text['dimensions']}
    Точный адрес отправки {text['shipping_address']}
    Точный адрес получения {text['receiving_address']}
    Способ оплаты {text['payment_method']}"""
    # Указываем путь к файлу шрифта Times New Roman
    font_path = "handlers/timesnewromanpsmt.ttf"

    # Загружаем шрифт
    pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))

    # Создание объекта Canvas (холст) для PDF с указанным путем к файлу
    c = canvas.Canvas(file_path, pagesize=letter)

    # Устанавливаем шрифт
    c.setFont("TimesNewRoman", 12)

    # Координаты начальной точки текста
    x = 100
    y = 750

    # Максимальная ширина текста на странице (может быть меньше, в зависимости от макета)
    max_width = 400

    # Разделитель строк
    line_height = 15

    # Разбиваем текст на строки
    lines = text_for_write.split('\n')

    # Начинаем отрисовку текста
    for line in lines:
        # Определяем ширину текущей строки текста
        width = c.stringWidth(line, "TimesNewRoman", 12)

        # Если ширина текста больше максимальной ширины, переносим текст на новую строку
        if width > max_width:
            c.drawString(x, y, line[:max_width])
            y -= line_height
            line = line[max_width:]

            # Переносим оставшуюся часть текста на следующую строку, если есть
            while len(line) > max_width:
                c.drawString(x, y, line[:max_width])
                y -= line_height
                line = line[max_width:]
            c.drawString(x, y, line)
        else:
            c.drawString(x, y, line)
        y -= line_height

    # Закрытие PDF
    c.save()



router = Router()

@router.message(F.text == '📑Начать заполнение дикларации')
@router.message(Command(commands=['fill_dec']))
async def fill_declaration(message: Message, state: FSMContext):
    await state.set_state(Declaration.about)
    await message.answer('Введите описание груза')

@router.message(Declaration.about)
async def fill_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(Declaration.weight)
    await message.answer('Введите вес груза')

@router.message(Declaration.weight)
async def fill_weight(message: Message, state: FSMContext):
    await state.update_data(weight = message.text)
    await state.set_state(Declaration.dimensions)
    await message.answer('Введите габариты')

@router.message(Declaration.dimensions)
async def fill_dimensions(message: Message, state: FSMContext):
    await state.update_data(dimensions=message.text)
    await state.set_state(Declaration.shipping_address)
    await message.answer('Введите точный адрес отправки')

@router.message(Declaration.shipping_address)
async def fill_shipping_adress(message: Message, state: FSMContext):
    await state.update_data(shipping_address=message.text)
    await state.set_state(Declaration.receiving_address)
    await message.answer('Введите Точный адрес получения')

@router.message(Declaration.receiving_address)
async def fill_receiving_adress(message: Message, state: FSMContext):
    await state.update_data(receiving_address=message.text)
    await state.set_state(Declaration.payment_method)
    await message.answer('Введите способ оплаты', reply_markup=builders.create_builder_reply(['Безналичные', 'Наличные'], one_time_keyboard=True))

@router.message(Declaration.payment_method)
async def fill_end(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(text='Супер, сейчас отправлю Вам pdf файл', reply_markup=builders.create_builder_reply('📑Начать заполнение дикларации'))
    create_pdf('handlers/test.pdf', data)
    input_file = FSInputFile("handlers/test.pdf", filename="handlers/test.pdf")
    await message.answer_document(input_file)