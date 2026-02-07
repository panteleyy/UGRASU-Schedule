from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F, types, Router
from datetime import datetime
from dotenv import load_dotenv
import os
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json
from aiogram.filters import BaseFilter


from functions import common_func, async_func
from keyboards import reply, inline

router = Router()

load_dotenv()
ADMIN_ID = int(os.getenv('ADMIN_ID'))

class BanState(StatesGroup): # Состояние бана
    waiting_user_id = State()

class IsAdmin(BaseFilter): # Класс админ
    async def __call__(self, event) -> bool:
        return event.from_user.id == ADMIN_ID

bot_disable = False

@router.callback_query(IsAdmin(), F.data == 'disable_bot')
async def bot_active(callback: CallbackQuery):
    global bot_disable
    bot_disable = True

    await callback.message.edit_reply_markup(reply_markup=inline.admin_keyboard_on)
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == 'enable_bot')
async def bot_active(callback: CallbackQuery):
    global bot_disable
    bot_disable = False

    await callback.message.edit_reply_markup(reply_markup=inline.admin_keyboard_off)
    await callback.answer()

class DisableBotMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        from_user = getattr(event, 'from_user', None)
        if not from_user:
            return await handler(event, data)

        if from_user.id == ADMIN_ID:
            return await handler(event, data)
        
        state = data.get("state")
        if state:
            current = await state.get_state()
            if current is not None:
                return await handler(event, data)

        if bot_disable:
            return

        return await handler(event, data)

@router.callback_query(F.data.startswith('faculty_'))
async def handle_faculty(callback: CallbackQuery):
    faculty_id = int(callback.data.split('_')[1])
    user_id = str(callback.from_user.id)

    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'facultyOid': faculty_id
    })

    common_func.save_configs(common_func.user_configs)

    await callback.answer()
    group_kb = common_func.find_groups(faculty_id)

    await callback.message.edit_text('Выбери группу:', reply_markup=group_kb)

@router.callback_query(F.data.startswith('group_'))
async def handle_group(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    group_id = int(callback.data.split('_')[1])


    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'group_id': group_id,
        'url_id': f'groupOid={group_id}',
        'who': 'student',
        'username': callback.from_user.username,
        'name': callback.from_user.full_name
    })

    group_name, facultyOid = common_func.get_group_name(callback, group_id)
    common_func.user_configs[user_id]['group_name'] = group_name

    common_func.save_configs(common_func.user_configs)

    await callback.answer()

    await callback.message.edit_text(f'Группа выбрана!')
    await callback.message.answer('Выбери действие:', reply_markup=reply.keyboard_look)
    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'theme': 'default'
    })

    common_func.save_configs(common_func.user_configs)

@router.callback_query(F.data.startswith('back_'))
async def handle_back_group(callback: CallbackQuery):
    await callback.message.edit_text('Выбери факультет:', reply_markup=common_func.find_faculties())

@router.callback_query(F.data.startswith('theme_'))
async def handle_themes(callback: CallbackQuery):
    theme_name = callback.data[len('theme_'):]
    user_id = str(callback.from_user.id)

    await callback.answer()
    
    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'theme': theme_name
    })

    common_func.save_configs(common_func.user_configs)

    await callback.message.answer('Тема выбрана!')

@router.callback_query(IsAdmin(), F.data == ('logs_bt')) # Отправка логов по кнопки с панели администратора
async def send_logs_bt(callback: CallbackQuery):
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S') # Дата и время прямо сейчас
    await callback.answer() # Закрываем часики
    await callback.message.answer_document(
        document=types.FSInputFile(path='logs.json'), 
        caption=f'Логи бота за {now_time}, requests - {async_func.request_counter}') # Отправка логов по кнопке

@router.callback_query(IsAdmin(), F.data == ('config_bt')) # Отправка конфига по кнопки с панели администратора
async def send_config_bt(callback: CallbackQuery):
    await callback.answer() # Закрываем часики
    await callback.message.answer_document(
        document=types.FSInputFile(path='user_settings.json'), 
        caption=f'Конфиг пользователей') # Отправка конфига по кнопке
    
@router.callback_query(IsAdmin(), F.data == 'bans_bt') # Отправка файла забанненых с панели администратора
async def send_bans_bt(callback: CallbackQuery):
    await callback.answer() # Закрываем часики
    await callback.message.answer_document(
        document=types.FSInputFile(path='banned_users.json'), 
        caption=f'Файл забаненных') 
    
@router.callback_query(IsAdmin(), F.data == 'hours_bt') # Отправка файла часовых запросов с панели администратора
async def send_hours_bt(callback: CallbackQuery):
    await callback.answer() # Закрываем часики
    await callback.message.answer_document(
        document=types.FSInputFile(path='hour_requests.json'), 
        caption=f'Часовые запросы') 
    
@router.callback_query(IsAdmin(), F.data == 'clear_logs_bt') # Удаление логов по кнопке
async def clear_logs(callback: CallbackQuery):
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    await callback.answer()
    
    try:
        try:
            await callback.message.answer_document(
                document=types.FSInputFile(path='logs.json'), 
                caption=f'[BACKUP] Логи бота за {now_time}, requests - {async_func.request_counter}') # Отправка логов 
            
            await callback.message.answer('✅ BACKUP')
        except Exception as e:
            await callback.message.answer(f'❌ BACKUP Ошибка: {e}')

        with open("logs.json", "w") as f: # Отчистка файла
            json.dump([], f) # Зпись в него [] что бы не был пустым
        
        async_func.request_counter = 0 # Обнуление счетчика запросов

        await callback.message.answer('✅ Логи удалены, счетчик отчищен')
    except Exception as e:
        await callback.message.answer(f'❌ Ошибка: {e}')

@router.callback_query(IsAdmin(), F.data == 'clear_chart_bt') # Очистка файла часовых запросов
async def clear_chart(callback: CallbackQuery):
    
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    await callback.answer()
    
    try:
        try:
            await callback.message.answer_document(
                document=types.FSInputFile(path='hour_requests.json'), 
                caption=f'[BACKUP] Часовые запросы бота за {now_time}, requests - {async_func.request_counter}') # Отправка логов 
            
            await callback.message.answer('✅ BACKUP')
        except Exception as e:
            await callback.message.answer(f'❌ BACKUP Ошибка: {e}')

        with open("hour_requests.json", "w") as f: # Отчистка файла
            json.dump([], f) # Зпись в него [] что бы не был пустым

        await callback.message.answer('✅ Файл с часовыми запросами удален')
    except Exception as e:
        await callback.message.answer(f'❌ Ошибка: {e}')

@router.callback_query(IsAdmin(), F.data == 'hours_chart_bt') # Очистка файла часовых запросов
async def send_hours_chart(callback: CallbackQuery):
    
    common_func.make_chart() # Создание графика из json
    
    photo = FSInputFile('chart.png')
    await callback.message.answer_photo(photo=photo) # Отправка
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == 'days_chart_bt') # Очистка файла часовых запросов
async def send_days_chart(callback: CallbackQuery):
    
    common_func.save_day_requests() # Создание графика из json
    
    photo = FSInputFile('day_chart.png')
    await callback.message.answer_photo(photo=photo) # Отправка
    await callback.answer()


@router.callback_query(IsAdmin(), F.data.startswith('ban_bt')) # Если Админ и ban_
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BanState.waiting_user_id) # Установка состояния "Ожидание айди"
    await callback.message.answer('Введите ID человека:', reply_markup=inline.chanel_ban_keyboard)
    await callback.answer()

@router.message(BanState.waiting_user_id) # Если Админ и состояние ожидания айди
async def process_ban(message: Message, state: FSMContext):
    if not message.text.isdigit(): # Если не цифры
        await message.answer('Нужен числовой ID!')
        return

    user_id = int(message.text)

    try: # Открытие json с забанеными
        with open('banned_users.json', 'r', encoding='utf-8') as file:
            banned_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_arr = []

    banned_arr.append(user_id) # Добавление айди человека в json с забанеными

    await message.answer(f'✅ Пользователь {user_id} забанен')

    with open('banned_users.json', 'w', encoding='utf-8') as banned_file: # Сохранение
        json.dump(banned_arr, banned_file, ensure_ascii=False, indent=4)

    await message.answer('✅ Изменения сохранены в json') 
    await state.clear() # Закрываем часики

@router.callback_query(IsAdmin(), F.data == 'cancel_ban') # Если в дате: cancel_ban и юзер Админ
async def cancel_ban(callback: CallbackQuery, state: FSMContext):
    await state.clear() # Чистим стейт, для отмены бана
    await callback.message.answer('❌ Бан отменён', reply_markup=reply.keyboard_look) 
    await callback.answer() # Убрали часики

@router.callback_query(IsAdmin(), F.data == 'unban_bt') # Если в дате: unban_bt и юзер Админ
async def ban_user(callback: CallbackQuery):
    try: # Открытие json с забанеными
        with open('banned_users.json', 'r', encoding='utf-8') as file:
            banned_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_arr = []

    if not banned_arr: # Если banned_arr пустой
        await callback.answer('❌ Нету забаненых')
    else: # Если не пустой
        await callback.message.answer('Выбери кого разбанить:', reply_markup=inline.unban_user_keyboard())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith('unban_')) # Если в дате: _unban и юзер - Админ
async def handle_group(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[1]) # Достаем айди забаненного из калбэка и переводим в int

    try: # Открытие json с забанеными 
        with open('banned_users.json', 'r', encoding='utf-8') as file:
            banned_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_arr = []

    banned_arr.remove(user_id) # Удаляем айди из json
    await callback.message.answer(f'✅ {user_id} - разбанен')

    with open('banned_users.json', 'w', encoding='utf-8') as f: # Сохранение изменений 
        json.dump(banned_arr, f, ensure_ascii=False, indent=2)

    await callback.message.answer('✅ Изменения сохранены в json')      
    await callback.answer() # Закрываем часики