import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.config import load_config
from tg_bot.filters.admin import AdminFilter
from tg_bot.handlers.admin import register_admin
from tg_bot.handlers.lost import register_lost
from tg_bot.handlers.user import register_user

from tg_bot.handlers.inline_keyboards import register_inline_keyboards

from tg_bot.services.sql_async import register_sql

from tg_bot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)

def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))

def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_inline_keyboards(dp)

    register_lost(dp)

def register_all_sql_handlers(dp):
    register_sql(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_sql_handlers(dp)
    register_all_handlers(dp)


    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
