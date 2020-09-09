import exceptions
from aquabalance import AquaBalanceBot

from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import bot, dp, logger, get_jedy, replicas


@dp.message_handler(
        state='*', commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Show hello message to help with bot"""
    logger.info(f"Send welcome handler text: {message.text} !")

    abot = await get_jedy(message.from_user.id, state)
    logger.info(f"is new user? {abot.new_user(message.from_user.username)}")

    await message.answer(replicas['start'])


@dp.message_handler(state='*', commands=['norm'])
async def norm(message: types.Message, state: FSMContext):
    """ Set norm parameter to X """
    logger.info(f"norm handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)
    try:
        x = int(message.text.split()[1])
    except ValueError:
        await message.answer(replicas['wrong_norm'])
        return
    except IndexError:
        return

    abot.update_norm(x)
    await message.answer(replicas['norm'])


@dp.message_handler(state='*', commands=['today'])
async def today(message: types.Message, state: FSMContext):
    """ Get drunk / norm in % """
    logger.info(f"today handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)

    vol = abot.today()
    await message.answer(replicas['today'] + str(vol) + '%')



@dp.message_handler(state='*', content_types=types.ContentTypes.TEXT)
async def add_drunk(message: types.Message, state: FSMContext):
    """ add one mark of drunk """
    logger.info(f"text handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)
    abot.add(message.text)
