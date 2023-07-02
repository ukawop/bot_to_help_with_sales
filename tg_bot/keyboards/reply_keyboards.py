from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Меню'),
    ],
],
    resize_keyboard=True)



adminka = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Меню'),
    ],
    [
        KeyboardButton(text='/admin'),
    ],
],
    resize_keyboard=True)
