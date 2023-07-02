from contextlib import suppress

from aiogram.dispatcher import FSMContext

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from tg_bot.keyboards.inline_keyboards import admin_menu, mailing_menu, mailing_access

from tg_bot.services.sql_async import get, mailing


async def admin_start(message: Message, state: FSMContext):
    await message.answer("Привет, админ!\nЧто ты хочешь сделать?", reply_markup=admin_menu)
    await state.reset_state()


class Mailing(StatesGroup):
    M1 = State()
    M2 = State()
    M3 = State()


async def mailing_start(call: CallbackQuery):
    await call.message.answer('Напиши что хочешь отправить. Можешь прикрепить фото с текстом или ссылку на видеоролик')
    await Mailing.M1.set()
    await call.answer()
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


async def mailing_photo(message: Message, state: FSMContext):
    await message.answer_photo(message.photo[-1].file_id, caption=message.caption)
    await message.answer('Так будет выглядить твое сообщение. Отменить?', reply_markup=mailing_access)
    answer1 = dict(photo=True, content=(message.photo[-1].file_id, message.caption))
    await state.update_data(answer1=answer1)


async def mailing_text(message: Message, state: FSMContext):
    await message.answer(message.text)
    await message.answer('Так будет выглядить твое сообщение. Изменить?', reply_markup=mailing_access)
    answer1 = dict(photo=False, content=message.text)
    await state.update_data(answer1=answer1)


async def mailing_accessing(call: CallbackQuery):
    await call.message.answer("Хочешь отправить ВСЕМ или выбрать конкретных?", reply_markup=mailing_menu)
    await Mailing.M2.set()
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


async def mailing_someone(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введити через пробел chat_id пользователей, которым хотите отправить сообщение\n'
                              'Можете посмотреть данные пользователей в главном меню /admin')
    await Mailing.M3.set()
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


async def mailing_someone_final(message: Message, state: FSMContext):
    users_id = message.text.split()
    data = await state.get_data()
    answer1 = data.get('answer1')
    if answer1['photo']:
        for users in users_id:
            try:
                await message.bot.send_photo(users, answer1['content'][0], answer1['content'][1])
            except Exception:
                pass
    else:
        for users in users_id:
            try:
                await message.bot.send_message(users, answer1['content'])
            except Exception:
                pass
    await state.reset_state()
    await message.answer('Сообщения доставлены')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", is_admin=True)
    dp.register_callback_query_handler(get, text_contains='get_file', is_admin=True)  # sql
    dp.register_callback_query_handler(mailing_start, text_contains='mailing', is_admin=True)
    dp.register_message_handler(mailing_photo, content_types=ContentTypes.PHOTO, state=Mailing.M1, is_admin=True)
    dp.register_message_handler(mailing_text, content_types=ContentTypes.TEXT, state=Mailing.M1, is_admin=True)
    dp.register_callback_query_handler(mailing_accessing, text_contains='select_users', state=Mailing.M1, is_admin=True)
    dp.register_callback_query_handler(mailing, text_contains='mailing_all', state=Mailing.M2, is_admin=True)  # sql
    dp.register_callback_query_handler(mailing_someone, text_contains='mailing_someones', state=Mailing.M2,
                                       is_admin=True)
    dp.register_message_handler(mailing_someone_final, state=Mailing.M3, is_admin=True)
