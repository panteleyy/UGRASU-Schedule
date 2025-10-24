from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from keyboards import inline, reply
from dictionary import const_dictionary
from functions import common_func, async_func

router = Router()

load_dotenv()
ADMIN_ID = int(os.getenv('ADMIN_ID'))
SECRET_WORD_LOGS = os.getenv('SECRET_WORD_LOGS')
SECRET_WORD_CONFIGS = os.getenv('SECRET_WORD_CONFIGS')

@router.message(Command('start'))
async def start_message(message: types.Message):
    update_text = (
    'Версия 1.0 «неРасписания ЮГУ» уже здесь! 🎉\n\n'
    'Что нового:\n\n'
    '📚 Просмотр расписания для всех факультетов и групп ЮГУ\n\n'
    '⚡ Более стабильная и быстрая работа благодаря переработанному коду\n\n'
    '🎨 Настраиваемые темы расписания — выбери свой стиль отображения /theme\n\n'
    '🛠 Улучшена обработка ошибок — теперь бот реже зависает(но это не точно)\n\n'
    '✨ Маленькие улучшения интерфейса для удобства использования\n\n'
    'Чтобы начать, выбери свою группу: /group\n\n'
    
)
    await message.answer(update_text)

@router.message(Command('theme'))
async def start_message(message: types.Message):
    await message.answer('Выбери тему:', reply_markup=inline.themes_keyboard())

@router.message(Command('info'))
async def group_command(message: types.Message):
    await message.answer('Команды бота:\n/start - полный перзапуск бота, смена группы\n/group - изменить группу\n/theme - изменить тему расписания\nСообщать о багах, предложениях и тд: @panteleeyy', reply_markup=reply.keyboard_look)

@router.message(Command('group'))
async def group_command(message: types.Message):
    await message.answer('Выбери факультет:', reply_markup=common_func.find_faculties())
@router.message(lambda message: 'расписание на сегодня' == message.text.lower())
async def ansewer(message: types.Message):
    today_date = datetime.today().date()
    day, month = common_func.date_to_text(today_date)
    weekday = common_func.get_weekday(today_date)

    await async_func.shedule_by_date(message, today_date, day, month, weekday)

@router.message(lambda message: 'расписание на завтра' == message.text.lower())
async def ansewer(message: types.Message):
    tommorow_date = datetime.today().date() + timedelta(days=1)
    day, month = common_func.date_to_text(tommorow_date)
    weekday = common_func.get_weekday(tommorow_date)

    await async_func.shedule_by_date(message, tommorow_date, day, month, weekday)

@router.message(lambda message: 'выбрать дату' == message.text.lower())
async def ansewer(message: types.Message):
    await message.answer('Выбери день', reply_markup=common_func.dates_to_keyboard())
@router.message(lambda message: any(month in message.text for month in const_dictionary.MONTHS.values()))
async def answer(message: types.Message):
    day, month = common_func.text_to_date(message.text)
    year = datetime.today().year
    
    user_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
    day, month = common_func.date_to_text(user_date)

    weekday_part = user_date.weekday()
    weekday = const_dictionary.WEEKDAYS.get(weekday_part) 

    await async_func.shedule_by_date(message, user_date, day, month, weekday)
    
@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_WORD_LOGS.lower())
async def what(message: types.Message):
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

    await message.answer_document(document=types.FSInputFile(path='logs.json'), caption=f'Логи бота за {now_time}, requests - {async_func.request_counter}')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_WORD_CONFIGS.lower())
async def what(message: types.Message):
    await message.answer('иба чотко')
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

    await message.answer_document(document=types.FSInputFile(path='user_settings.json'), caption=f'Конфиг пользователей за {now_time}')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)