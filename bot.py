#########################################################
#                      БИБЛИОТЕКИ                       #
#########################################################

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#########################################################
#                        МОДУЛИ                         #
#########################################################

from config import TOKEN
from utils import TestStates
from messages import MESSAGES
from owm import ReturnWeather
from random import randint
from sqliter import SQLighter
from sqliter import SQLreader
from time_checker import TimeChecker
import markups as nav

#########################################################
#                    ИНИЦИАЛИЗАЦИЯ                      #
#########################################################

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db.db')
db_out = SQLreader('db.db')

#########################################################
#                        КОМАНДЫ                        #
#########################################################

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    db.add_subscriber(message.from_user.id)
    await message.reply(MESSAGES['start'], reply_markup = nav.mainMenu, reply=False)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):

    await message.reply(MESSAGES['help'], reply=False)

#########################################################
#                  ОБРАБОТКА СООБЩЕНИЙ                  #
#########################################################

@dp.message_handler()
async def sorting_messages(message: types.Message):

    if message.text == "Главное меню":
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await bot.send_message(message.from_user.id, MESSAGES['what'], reply_markup = nav.mainMenu)

 
    elif message.text == 'Узнать погоду':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[1])
        nav.RaisingWeatherMenu(message.from_user.id)
        await bot.send_message(message.from_user.id, MESSAGES['ask_place'],reply_markup = nav.weatherMenu)

    elif message.text == 'Рандомное число':
        await bot.send_message(message.from_user.id, f'Ваше число: {randint(-1000000,1000000)}')

    elif message.text == 'О боте':
        await message.reply(MESSAGES['help'], reply=False)

#########################################################
#                        ПОГОДА                         #
#########################################################

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def weather_filter(message: types.Message):

    if message.text == "Главное меню":
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await bot.send_message(message.from_user.id, MESSAGES['what'],reply_markup = nav.mainMenu)

    elif message.text == 'Потсавить оповещение':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[2])
        await bot.send_message(message.from_user.id, MESSAGES['rem_set'],reply_markup = nav.remindingMenu)

    else:
        city = message.text
        print(city)
        state = dp.current_state(user=message.from_user.id)
        asnwer = ReturnWeather(city)

        if asnwer == "Вы ошиблись в названии города":
            await bot.send_message(message.from_user.id, f'{asnwer}\n' + MESSAGES['try_again'])

        else:
            await bot.send_message(message.from_user.id, f'{asnwer}',reply_markup = nav.mainMenu)
            await state.reset_state()
            db.set_latest_place(message.from_user.id, city)
            print(db_out.read_informarion(message.from_user.id))

#########################################################
#                     ОПОВЕЩЕНИЯ                        #
#########################################################

@dp.message_handler(state=TestStates.TEST_STATE_2)
async def reminding_ilter(message: types.Message):

    if message.text == 'Указать город':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[3])
        await bot.send_message(message.from_user.id, MESSAGES['ask_place'], reply_markup = nav.remSetMenu)

    elif message.text == 'Установить часовой пояс':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[4])
        await bot.send_message(message.from_user.id, MESSAGES['utc'], reply_markup = nav.remSetMenu)

    elif message.text == 'Указать время напоминания':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[5])
        await bot.send_message(message.from_user.id, MESSAGES['time'], reply_markup = nav.remSetMenu)

    elif message.text == 'Назад':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[1])
        await bot.send_message(message.from_user.id, MESSAGES['ask_place'],reply_markup = nav.weatherMenu)

#########################################################
#                   МЕСТО ОПОВЕЩЕНИЯ                    #
#########################################################

@dp.message_handler(state=TestStates.TEST_STATE_3)
async def reminding_ilter(message: types.Message):

    if message.text == 'Назад':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[2])
        await bot.send_message(message.from_user.id, MESSAGES['rem_set'],reply_markup = nav.remindingMenu)
    
    elif message.text == 'Главное меню':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await bot.send_message(message.from_user.id, MESSAGES['what'], reply_markup = nav.mainMenu)

    else:
        city = message.text
        print(city)
        state = dp.current_state(user=message.from_user.id)
        asnwer = ReturnWeather(city)

        if asnwer == "Вы ошиблись в названии города":
            await bot.send_message(message.from_user.id, f'{asnwer}\n' + MESSAGES['try_again'])

        else:
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(TestStates.all()[2])
            db.set_place(message.from_user.id, city)
            await bot.send_message(message.from_user.id, f"{MESSAGES['s_place']}\n{MESSAGES['next_tip']}",reply_markup = nav.remindingMenu)

#########################################################
#                ЧАСОВОЙ ПОЯС ОПОВЕЩЕНИЯ                #
#########################################################

@dp.message_handler(state=TestStates.TEST_STATE_4)
async def reminding_ilter(message: types.Message):

    if message.text == 'Назад':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[2])
        await bot.send_message(message.from_user.id, MESSAGES['rem_set'],reply_markup = nav.remindingMenu)

    elif message.text == 'Главное меню':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await bot.send_message(message.from_user.id, MESSAGES['what'], reply_markup = nav.mainMenu)

    else:
        UTC = int(message.text)

        if UTC >= 0 and UTC < 24:
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(TestStates.all()[2])
            db.set_UTC(message.from_user.id, UTC)
            await bot.send_message(message.from_user.id, f"{MESSAGES['s_UTC']}\n{MESSAGES['next_tip']}",reply_markup = nav.remindingMenu)
        
        else:
            await bot.send_message(message.from_user.id, MESSAGES['try_again'])


#########################################################
#                   ВРЕМЯ ОПОВЕЩЕНИЯ                    #
#########################################################

@dp.message_handler(state=TestStates.TEST_STATE_5)
async def reminding_ilter(message: types.Message):

    if message.text == 'Назад':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[2])
        await bot.send_message(message.from_user.id, MESSAGES['rem_set'],reply_markup = nav.remindingMenu)

    elif message.text == 'Главное меню':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await bot.send_message(message.from_user.id, MESSAGES['what'], reply_markup = nav.mainMenu)

    else:

        if TimeChecker(message.text):
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(TestStates.all()[2])
            db.set_time(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id,f"{MESSAGES['s_time']}\n{MESSAGES['next_tip']}",reply_markup = nav.remindingMenu)
        
        else:
             await bot.send_message(message.from_user.id, MESSAGES['try_again'])

#########################################################
#             ОТКЛЮЧЕНИЕ МАШИНЫ СОСТОЯНИЙ               #
#########################################################

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

#########################################################
#                      ИСПОЛНЕНИЕ                       #
#########################################################

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)