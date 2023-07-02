from contextlib import suppress

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from tg_bot.keyboards.inline_keyboards import main_menu, return_menu

from tg_bot.photo_and_caption import *


async def show_main_menu(message: Message):
    await message.answer_photo(photo_main, main_caption, reply_markup=main_menu)


async def button_1(call: CallbackQuery):
    await call.message.answer_photo(photo_1, caption=caption_1, reply_markup=return_menu)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

async def button_2(call: CallbackQuery):
    await call.message.answer_photo(photo_2, caption=caption_2, reply_markup=return_menu)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

async def button_3(call: CallbackQuery):
    await call.message.answer_photo(photo_3, caption=caption_3, reply_markup=return_menu)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

async def button_4(call: CallbackQuery):
    await call.message.answer_photo(photo_4, caption=caption_4, reply_markup=return_menu)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

async def return_main_menu(call: CallbackQuery):
    await call.message.answer_photo(photo_main, main_caption, reply_markup=main_menu)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, Text(equals=['Меню']))
    dp.register_callback_query_handler(button_1, text_contains='1к')
    dp.register_callback_query_handler(button_2, text_contains='2к')
    dp.register_callback_query_handler(button_3, text_contains='3к')
    dp.register_callback_query_handler(button_4, text_contains='4к')
    dp.register_callback_query_handler(return_main_menu, text_contains='menu')
