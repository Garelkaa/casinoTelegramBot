from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiocryptopay import Networks, AioCryptoPay

from database.requests import UserDb
from loader_cfg import TOKEN, api_token_pay


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
userdb = UserDb()
crypto = AioCryptoPay(token=api_token_pay, network=Networks.TEST_NET)
