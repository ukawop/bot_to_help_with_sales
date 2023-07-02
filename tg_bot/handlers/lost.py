from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.utils.markdown import hcode


async def bot_all_photo(message: types.Message):
    text = [
        "id присланной вами фотографии:\n",
        message.photo[-1].file_id,
    ]

    await message.answer('\n'.join(text))


async def bot_all(message: types.Message):
    await message.answer('Такой команды нет. Нажмите /start')

def register_lost(dp: Dispatcher):
    dp.register_message_handler(bot_all_photo, content_types=ContentTypes.PHOTO)
    dp.register_message_handler(bot_all, state="*", content_types=types.ContentTypes.ANY)