from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
from aiogram import BaseMiddleware
import json
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode

from keyboards import inline, reply
from dictionary import const_dictionary
from functions import common_func, async_func, teachers_file

router = Router()

load_dotenv()
ADMIN_ID = int(os.getenv('ADMIN_ID'))
SECRET_WORD_LOGS = os.getenv('SECRET_WORD_LOGS')
SECRET_WORD_CONFIGS = os.getenv('SECRET_WORD_CONFIGS')
API_BASE_URL = os.getenv('API_BASE_URL')
SECRET_ADMIN_WORD = os.getenv('SECRET_ADMIN_WORD')
SECRET_CHART_WORD = os.getenv('SECRET_CHART_WORD')
SECRET_DAY_CHART_WORD = os.getenv('SECRET_DAY_CHART_WORD')

class TeacherState(StatesGroup):
    waiting_name = State()

class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if not user:
            return await handler(event, data)

        try:
            with open('banned_users.json', 'r', encoding='utf-8') as f:
                banned = json.load(f)
        except:
            banned = []

        if user.id in banned and user.id != ADMIN_ID:
            return  

        return await handler(event, data)

@router.message(Command('start'))
async def start_message(message: types.Message, command: Command):

    user_id = str(message.from_user.id)

    if command.args:

        today_date = datetime.today().date()
        day, month = common_func.date_to_text(today_date)
        weekday = common_func.get_weekday(today_date)

        if command.args and command.args.startswith('teacher_'):
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            url_id = command.args.replace('teacher_', 'lecturerOid=')

            for t in teachers_file.teacher_file:
                if t["lecturerOid"] == int(url_id.replace('lecturerOid=', '')):
                    group_name = t['fio']

        elif command.args and command.args.startswith('cab_'):
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            url_id = command.args.replace('cab_', 'auditoriumOid=')

            group, auditorium_id = common_func.get_cabinet_info(None, int(url_id.replace('auditoriumOid=', '')))
            group_name = 'Кабинет: ' + group
                
        await async_func.shedule_by_date_link(message, 
                                                today_date, 
                                                day, 
                                                month, 
                                                weekday, 
                                                user_id, 
                                                url_id,  
                                                group_name)

    else:

        update_text = (
        '👋 Привет! Это бот для просмотра расписания занятий в ЮГУ\n\n'
        '👥 Для того что бы посмотреть расписание нужно выбрать группу или преподавателя: /group или /teacher\n\n'
        '🎨 Так же можно изменить тему отабражения расписания: /theme\n\n' \
        "<blockquote>"
        "Бот разработан студентом и не имеет официального отношения к ЮГУ."
        "</blockquote>\n\n"
        'ℹ️ Больше информации: /info')

        await message.answer(update_text, parse_mode=ParseMode.HTML, reply_markup=reply.keyboard_look)

@router.message(Command('theme')) # ВЫБОР ТЕМЫ
async def start_message(message: types.Message):
    await message.answer('Выбери тему:', reply_markup=inline.themes_keyboard())

@router.message(Command('info')) # ИНФОРМАЦИЯ О БОТЕ
async def group_command(message: types.Message):
    text = (
        "⚙️ Команды бота\n\n"
        "/start — полный перезапуск бота, смена группы\n"
        "/group — изменить группу\n"
        "/theme — изменить тему расписания\n" \
        "/changelog - список нововедений\n\n" \
        "<blockquote>"
        "Бот разработан студентом и не имеет официального отношения к ЮГУ."
        "</blockquote>\n\n"
        "Сообщать о багах и предложениях: @panteleeyy"
    )

    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=reply.keyboard_look)

@router.message(Command('group')) # ВЫБОР ГРУППЫ
async def group_command(message: types.Message):
    await message.answer('Выбери факультет:', reply_markup=common_func.find_faculties())

@router.message(Command('changelog')) # ЧЕЙНДЖОЛОГ
async def changelog(message: types.Message):
    await message.answer(
    "Версия 1.1 «неРасписания ЮГУ» уже тут! 🚀\n\n"
    "👨‍🏫 Добавлена возможность смотреть расписание преподавателей: /teacher\n\n"
    "🔧 Исправлены ошибки, повышена стабильность работы бота\n\n"
    "Если бот не отвечает писать: @panteleeyy\nСпасибо, что пользуетесь ботом!")

### РАСПИСАНИЕ НА СЕГОДНЯ ###

@router.message(lambda message: 'расписание на сегодня' == message.text.lower())
async def ansewer(message: types.Message):

    user_id = str(message.from_user.id)

    if user_id in common_func.user_configs:
        common_func.user_configs[user_id]['await_teacher'] = False
        common_func.user_configs[user_id]['username'] = message.from_user.username
        common_func.save_configs(common_func.user_configs)

    today_date = datetime.today().date()
    day, month = common_func.date_to_text(today_date)
    weekday = common_func.get_weekday(today_date)

    
    url_id = common_func.user_configs.get(user_id, {}).get('url_id')

    await async_func.shedule_by_date(message, today_date, day, month, weekday, user_id, url_id)

### РАСПИСАНИЕ НА ЗАВТРА ###

@router.message(lambda message: 'расписание на завтра' == message.text.lower())
async def ansewer(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id in common_func.user_configs:
        common_func.user_configs[user_id]['await_teacher'] = False
        common_func.user_configs[user_id]['username'] = message.from_user.username
        common_func.save_configs(common_func.user_configs)

    tommorow_date = datetime.today().date() + timedelta(days=1)
    day, month = common_func.date_to_text(tommorow_date)
    weekday = common_func.get_weekday(tommorow_date)

    
    url_id = common_func.user_configs.get(user_id, {}).get('url_id')

    await async_func.shedule_by_date(message, tommorow_date, day, month, weekday, user_id, url_id)

### # РАСПИСАНИЕ ПО ВЫБРАННОЙ ДАТЕ ###

@router.message(lambda message: 'выбрать дату' == message.text.lower()) 
async def ansewer(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id in common_func.user_configs:
        common_func.user_configs[user_id]['await_teacher'] = False
        common_func.save_configs(common_func.user_configs)

    await message.answer('Выбери день', reply_markup=common_func.dates_to_keyboard())
@router.message(lambda message: any(month in message.text for month in const_dictionary.MONTHS.values()))
async def answer(message: types.Message):

    user_id = str(message.from_user.id)

    if user_id in common_func.user_configs:
        common_func.user_configs[user_id]['await_teacher'] = False
        common_func.save_configs(common_func.user_configs)

    day, month = common_func.text_to_date(message.text)
    year = datetime.today().year
    
    user_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
    day, month = common_func.date_to_text(user_date)

    weekday_part = user_date.weekday()
    weekday = const_dictionary.WEEKDAYS.get(weekday_part)

    
    url_id = common_func.user_configs.get(user_id, {}).get('url_id')

    await async_func.shedule_by_date(message, user_date, day, month, weekday, user_id, url_id)
    
### АДМИН ПАНЕЛЬКА ###

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_ADMIN_WORD.lower())
async def admin_panel(message: types.Message):

    current_date = datetime.now().strftime('%d.%m')
    current_hour = datetime.now().strftime('%d.%m - %H') # Текущий час + дата

    hour = 0
    day = 0
    users = 0
    active_users = 0

    with open('hour_requests.json', 'r', encoding='utf-8') as f:
        hour_requests = json.load(f)

    with open('user_settings.json', 'r', encoding='utf-8') as f:
        user_settings = json.load(f)

    for item in hour_requests:
        date_path, hour_path = item['date'].split(' - ')

        if item['date'] == current_hour:
            hour = item['hour_requests']

        if date_path == current_date:
            day += item['hour_requests']

    for usr in user_settings:
        if usr:
            users += 1

        if 'last_request' in user_settings[usr]:
            try:
                last_request_time = datetime.strptime(user_settings[usr]['last_request'], '%d.%m.%Y - %H:%M:%S')
                time_diff = datetime.now() - last_request_time
                if time_diff <= timedelta(days=3):
                    active_users += 1
            except (ValueError, TypeError):
                
                continue


    text = ('🏢 Панелька администратора:\n'
    '━━━━━━━━━━━━━━━\n'
    f'⏱ Час: {hour}\n'
    f'📅 Сегодня: {day}\n'
    f'👥 Пользователей: {users}\n'
    f'🗣 Активных пользователей: {active_users}')

    await message.answer(text, reply_markup=inline.admin_keyboard_off)

### КОМАНДЫ ДЛЯ ПОЛУЧЕНИЯ ФАЙЛОВ И ГРАФИКОВ, АДМИНИСТРАТОРОМ ###

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_WORD_LOGS.lower()) # Получение логов
async def send_logs(message: types.Message):
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

    await message.answer_document(document=types.FSInputFile(path='logs.json'), caption=f'Логи бота за {now_time}, requests - {async_func.request_counter}')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_WORD_CONFIGS.lower()) # Получение конфига
async def send_config(message: types.Message):
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

    await message.answer_document(document=types.FSInputFile(path='user_settings.json'), caption=f'Конфиг пользователей за {now_time}')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_CHART_WORD.lower()) # Получение графика по часам
async def send_chart(message: types.Message):
    common_func.make_chart() # Создание графика из json
    
    photo = FSInputFile('chart.png')
    await message.answer_photo(photo=photo) # Отправка
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@router.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.lower() == SECRET_DAY_CHART_WORD.lower()) # Получение графика по дням
async def send_chart(message: types.Message):
    common_func.save_day_requests()  # Создание графика из json
    
    photo = FSInputFile('day_chart.png')
    await message.answer_photo(photo=photo) # Отправка
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


### ВЫБОР ПРЕПОДАВАТЕЛЯ ###

@router.message(Command('teacher')) 
async def teachers(message: Message, state: FSMContext):
    await state.set_state(TeacherState.waiting_name)
    await message.answer(
        'Напишите ФИО преподавателя, по примеру: Иванов И И\n(Регистр не имеет значения)'
    )
@router.message(TeacherState.waiting_name)
async def process_teacher(message: Message, state: FSMContext):
    user_input = message.text.lower().strip()
    teacher_id = teachers_file.get_teacheroid(user_input)

    if teacher_id is None:
        await message.answer('❌ Преподаватель не найден, попробуйте еще раз')
        return

    user_id = str(message.from_user.id)

    common_func.user_configs.setdefault(user_id, {})
    common_func.user_configs[user_id].update({
        'group_id': teacher_id,
        'url_id': f'lecturerOid={teacher_id}',
        'theme': 'default',
        'who': 'teacher',
        'name': message.from_user.full_name,
        'username': message.from_user.username,
    })

    group_name, facultyOid = common_func.get_group_name(message, teacher_id)
    common_func.user_configs[user_id]['group_name'] = group_name
    common_func.user_configs[user_id]['username'] = message.from_user.username
    common_func.save_configs(common_func.user_configs)

    await message.answer(f'✅ Преподаватель выбран')
    await state.clear()


    

