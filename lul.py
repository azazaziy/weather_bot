from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time

#########################################################
#                        МОДУЛИ                         #
#########################################################

from config import TOKEN
from utils import TestStates
from messages import MESSAGES
from owm import ReturnWeather
from random import randint
from sqliter import SQLighter
from time_checker import TimeChecker
import markups as nav

#########################################################
#                    ИНИЦИАЛИЗАЦИЯ                      #
#########################################################

bot = Bot(token='993509427:AAE97Cmr86JD9SRRQon3zja9ljWt1lOHvIo')
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db.db')


@dp.message_handler()
async def sorting_messages(message: types.Message):
	if message.text == '123123':
		while True:
			await bot.send_message(459834054, MESSAGES['ask_place'],reply_markup = nav.weatherMenu)
			time.sleep(0.3)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
