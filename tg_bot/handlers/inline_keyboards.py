from contextlib import suppress

from aiogram.dispatcher import FSMContext

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound


async def cancel_main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer('закрыто!')
    await state.reset_state()
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()




def register_inline_keyboards(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_main_menu, state='*', text_contains='cancel')