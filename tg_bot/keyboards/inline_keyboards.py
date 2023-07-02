from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🏢 О Компании',callback_data='1к'),
        InlineKeyboardButton(text='2 кнопка',callback_data='2к')
    ],
    [
        InlineKeyboardButton(text='3 кнопка',callback_data='3к'),
        InlineKeyboardButton(text='4 кнопка',callback_data='4к')
    ],
    [
        InlineKeyboardButton(text='↩Отмена',callback_data='cancel')
    ],
])

return_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Меню',callback_data='menu'),
    ],
])

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Данные',callback_data='get_file'),
        InlineKeyboardButton(text='Рассылка',callback_data='mailing')
    ],
    [
        InlineKeyboardButton(text='↩Отмена', callback_data='cancel')
    ],
])

mailing_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Всем',callback_data='mailing_all'),
        InlineKeyboardButton(text='Выбрать кому',callback_data='mailing_someones')
    ],
    [
        InlineKeyboardButton(text='↩Отмена', callback_data='cancel')
    ],
])

mailing_access = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Указать получателей',callback_data='select_users'),
    ],
    [
        InlineKeyboardButton(text='↩Отмена', callback_data='cancel')
    ],
])
