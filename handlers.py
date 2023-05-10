from aiogram import types
from aiogram.dispatcher import FSMContext
from misc import bot, dp, logger, get_jedy, replicas
from random import choice


yes_sticker = 'CAACAgIAAxkBAAEBUFhfWKde9cDBGdMIB6khGi-MYk24uAACRAADQbVWDFpIqKL_emcUGwQ'
rand_glass_stickers = ['CAACAgIAAxkBAAEBUDxfWKQhYTWMlTwtWI9xjbnRBHp6gAACTQADKA9qFJeLFU6mcatiGwQ',
'CAACAgIAAxkBAAEBUD5fWKRFnGN1AAFspeJV8i28UiYTmJMAAk4AAygPahRTzIx8k3rZIRsE',
'CAACAgIAAxkBAAEBUEBfWKRW8569a2jtIC_AmVhJndWZ-wACSwADKA9qFNoPqQbjuZ_LGwQ',
'CAACAgIAAxkBAAEBUEJfWKRrEF_Pok5QT3mZyN2h184m0AACPwADKA9qFGqgL_9ebv15GwQ',
'CAACAgIAAxkBAAEBUERfWKSG7GhDj4WvPvx-zVteYJ0eKQACRAADKA9qFFts_7_cyqtAGwQ',
'CAACAgIAAxkBAAEBUEZfWKSXu_zSe9cvAYaY2FT2tx_JjgACQQADKA9qFPDp0yN1HEZhGwQ',
'CAACAgIAAxkBAAEBUEhfWKSpd0VZuj3_ibfqZrOSvrx5tQACRwADKA9qFDTwM1GiIoFsGwQ',
'CAACAgIAAxkBAAEBUEpfWKS3JEX6zU-Y4VdmCqV_KL3tKQACLwADKA9qFMV3-0AJ5TN3GwQ',
'CAACAgIAAxkBAAEBUExfWKTIiuZAwJouKnUHJDW5ldGrXQACMgADKA9qFGUiobSLpOJLGwQ',
'CAACAgIAAxkBAAEBUE5fWKTdWWGZqMbJ7-AuK3oFHLxrwQACLAADKA9qFBrFj1UD5bkFGwQ',
'CAACAgIAAxkBAAEBUFJfWKTxuzeEuojxbWeurVMzvFjVAAMpAAMoD2oUt8YUgo85goYbBA',
'CAACAgIAAxkBAAEBUFZfWKUVkKrchVv5RqMSrvSBDs0I6QACMQADKA9qFNP_vQUM1nJIGwQ']


@dp.message_handler(
        state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Show hello message to help with bot"""
    logger.info(f"Send welcome handler text: {message.text} !")

    abot = await get_jedy(message.from_user.id, state)
    logger.info(f"is new user? {abot.new_user(message.from_user.username)}")

    kb_markup = types.ReplyKeyboardMarkup(row_width=2)
    btns_text = ('/glass', '/total')
    kb_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    await message.answer(replicas['start'], reply_markup=kb_markup)


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


@dp.message_handler(state='*', commands=['total'])
async def today(message: types.Message, state: FSMContext):
    """ Show drunk / norm in % """
    logger.info(f"today handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)

    vol = abot.total()
    await message.answer(replicas['today'] + str(vol) + '%')


@dp.message_handler(state='*', commands=['glass'])
async def today(message: types.Message, state: FSMContext):
    """ add one glass (250 ml) """
    logger.info(f"glass handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)

    abot.add('250')

    sticker = yes_sticker if abot.check() else choice(rand_glass_stickers)
    await bot.send_sticker(message.from_user.id, sticker)


@dp.message_handler(state='*', content_types=types.ContentTypes.TEXT)
async def add_drunk(message: types.Message, state: FSMContext):
    """ add one mark of drunk """
    logger.info(f"text handler {message.text}")
    abot = await get_jedy(message.from_user.id, state)
    abot.add(message.text)

    sticker = yes_sticker if abot.check() else choice(rand_glass_stickers)
    await bot.send_sticker(message.from_user.id, sticker)
