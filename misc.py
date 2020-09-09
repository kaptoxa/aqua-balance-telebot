import logging


import os
import json

from aquabalance import AquaBalanceBot

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open("replicas.json", "r") as r_file:
    replicas = json.load(r_file)



async def get_jedy(chat_id, state: FSMContext):
    """ while storage is memory
        we need to create TaskListBot object
        every time after restart """

    data = await state.get_data()
    if 'bot' not in data:
        new_bot = AquaBalanceBot(chat_id)
        await state.update_data(bot=new_bot)
        return new_bot

    return data['bot']
