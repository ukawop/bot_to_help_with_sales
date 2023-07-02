from contextlib import suppress

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from tg_bot.config import load_config
from tg_bot.keyboards.reply_keyboards import menu, adminka

from aiogram import Dispatcher
from aiogram.types import Message, InputFile


import asyncio
import asyncpg
from asyncpg.exceptions import UniqueViolationError

config = load_config('.env')


async def create_table():
    conn = await asyncpg.connect(host=config.db.host,
                                 user=config.db.user,
                                 password=config.db.password,
                                 database=config.db.database,
                                 port='5432')
    await conn.execute('''create table if not exists users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    id        bigint            not null,
    language  text,
    data_start timestamp
);'''
                       )
    await conn.close()

asyncio.get_event_loop().run_until_complete(create_table())

async def add_new_user1(message: Message):
    chat_id = str(message.chat.id)
    username = str(message.from_user.username) or 'null'
    full_name = str(message.from_user.full_name)
    id = str(message.from_user.id)
    language = str(message.from_user.language_code)

    conn = await asyncpg.connect(host=config.db.host,
                                 user=config.db.user,
                                 password=config.db.password,
                                 database=config.db.database,
                                 port='5432')
    try:
        await conn.execute(f'''INSERT INTO users (chat_id, username, full_name, id, language, data_start)
                     VALUES ({chat_id},'{username}','{full_name}',{id},'{language}', NOW());''')
    except UniqueViolationError as ex:
        pass
    await conn.close()

async def get_file(call):
    path = "Users_data.xlsx"
    conn = await asyncpg.connect(host=config.db.host,
                                 user=config.db.user,
                                 password=config.db.password,
                                 database=config.db.database,
                                 port='5432')
    await conn.copy_from_query('Select * from users', output=path, format='csv')
    await conn.close()
    await call.message.answer_document(InputFile(path))


async def mailing_all(call, state):
    conn = await asyncpg.connect(host=config.db.host,
                                 user=config.db.user,
                                 password=config.db.password,
                                 database=config.db.database,
                                 port='5432')
    users_id = await conn.fetch(f'''SELECT chat_id FROM users;''')
    data = await state.get_data()
    answer1 = data.get('answer1')
    if answer1['photo']:
        for users in users_id:
            try:
                await call.bot.send_photo(users[0], answer1['content'][0],answer1['content'][1] )
            except Exception:
                pass
    else:
        for users in users_id:
            try:
                await call.bot.send_message(users[0], answer1['content'] )
            except Exception:
                pass
    await conn.close()
    await call.message.answer('Сообщения доставлены')
    await state.reset_state()


async def add(message, state):
    await message.answer('Здравствуйте, для входа в главное меню нажмите - Меню ⬇', reply_markup=menu)
    await asyncio.get_event_loop().create_task(add_new_user1(message))
    await state.reset_state()

async def add_admin(message, state):
    await message.answer('Здравствуйте, для входа в главное меню нажмите - Меню ⬇', reply_markup=adminka)
    await asyncio.get_event_loop().create_task(add_new_user1(message))
    await state.reset_state()


async def get(call):
    await asyncio.get_event_loop().create_task(get_file(call))
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

async def mailing(call, state):
    await asyncio.get_event_loop().create_task(mailing_all(call, state))
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()



def register_sql(dp: Dispatcher):
    dp.register_message_handler(add_admin, commands=['start'], is_admin=True)
    dp.register_message_handler(add, commands=['start'])
    dp.register_message_handler(get, commands=['getfile'])
