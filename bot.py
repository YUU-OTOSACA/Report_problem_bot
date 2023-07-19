import asyncio
from distutils.cmd import Command
import logging
import csv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.base import String
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from app.config_reader import load_config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

logger = logging.getLogger(__name__)

config = load_config("config/bot.ini")

credentials = ServiceAccountCredentials.from_json_keyfile_name(config.tg_bot.json, scope)
client = gspread.authorize(credentials)

bot = Bot(token=config.tg_bot.token)

number = 1

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config = load_config("config/bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_report(dp)

    await set_commands(bot)

    await dp.start_polling()

async def cmd_start(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Сообщить о проблеме"]
    keyboard.add(*buttons)

    await message.answer("Привет, если у тебя возникли проблемы с оборудованием, то напиши мне.", reply_markup=keyboard)

class Problem_Report(StatesGroup):
    names = State()
    problems = State()
    create_databases = State()

async def report_start(message: types.Message, state: FSMContext):
    await message.answer('Напишие ваши ФИО полностью', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Problem_Report.names.state)

async def NAME(message: types.Message, state: FSMContext):
    await state.update_data(NAMES=message.text.lower())

    await state.set_state(Problem_Report.problems.state) 
    await message.answer('Опишите вашу проблему')

async def PROBLEM(message: types.Message, state: FSMContext):

    await state.update_data(PROBLEMS=message.text.lower())

    user_data = await state.get_data()

    await message.answer(f"Вот текст вашего обращения:\"{user_data['NAMES']}. {user_data['PROBLEMS']}\"\n ", parse_mode="HTML")
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Всё верно", "Изменить"]
    keyboard.add(*buttons)
    await message.answer('Всё верно?', reply_markup=keyboard)

    await state.reset_state(with_data=False)

async def report(message: types.Message, state:FSMContext):

    global number

    config = load_config("config/bot.ini")

    user_data = await state.get_data()

    await message.answer('Ваша заявка отправлена', reply_markup=types.ReplyKeyboardRemove())
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Сообщить о проблеме"]
    keyboard.add(*buttons)

    await message.answer('У вас появились ещё проблемы?', reply_markup=keyboard)
    
    text_problem = user_data['NAMES'] + "." + user_data['PROBLEMS']

    await bot.send_message(chat_id = config.tg_bot.admin_id, text =  text_problem)

    with open("classmates.csv", mode="a", encoding='utf-8') as a_file:
        global number
        file_writer = csv.writer(a_file, delimiter = ",", lineterminator="\r")
        file_writer.writerow([number, user_data['NAMES'], user_data['PROBLEMS']])

    number = number + 1
    sheet = client.open(config.tg_bot.sheet_name).sheet1

    df = pd.read_csv('classmates.csv')

    sheet.update([df.columns.values.tolist()] + df.values.tolist())


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(report_start, lambda message: message.text == "Сообщить о проблеме", state="*")
    dp.register_message_handler(NAME, state=Problem_Report.names)
    dp.register_message_handler(PROBLEM, state=Problem_Report.problems)
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(report_start, lambda message: message.text == "Изменить", state="*")
    dp.register_message_handler(report, lambda message: message.text == "Всё верно", state="*")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command = '/start',  description='Начать')
    ]


if __name__ == '__main__':
    asyncio.run(main())