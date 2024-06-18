import sys
import logging
import asyncio

from signature import bot, dp
from middleware.subs import CheckSub
from database.models import async_main
from middleware.settings import StateBot
from handlers.registers import HandlersSetup


async def start_up():
    handlers_setup = HandlersSetup(dp)
    await handlers_setup.setup_start()


async def main():
    await async_main()
    await start_up()

    dp.message.middleware(StateBot())
    #dp.message.middleware(CheckSub())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
