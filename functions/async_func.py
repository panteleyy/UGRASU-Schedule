import json
from matplotlib import text
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import bot

from functions import common_func
from keyboards import reply
from shedule_themes import theme
from functions import teachers_file


load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

request_counter = 0

async def shedule_by_date(message, date, day, month, weekday, user_id, url_id):

    group_id = common_func.user_configs.get(user_id, {}).get('group_id') # Получаем айди выбранной группы или преподавателя

    if not group_id: # Проверка на наличе группы
        await message.answer('Сначала выбери группу /group или преподавателя /teacher, а лучше посмотри изменения новой версии /changelog')
        return
    
    url = f'{API_BASE_URL}/lessons?fromdate={date}&todate={date}&{url_id}'
    
    try:
        async with message.bot.aiohttp_session.get(url) as response:
            if response.status != 200:
                await message.answer(f'⚠️ Ошибка сервера, попробуйте позже')
                return

            lessons_file = await response.json()
            lessons_sorted = sorted(lessons_file, key=lambda x: (datetime.strptime(x['date'], '%Y.%m.%d'), x['beginLesson']))

        date_lessons = [
            l for l in lessons_sorted
            if datetime.strptime(l["date"], "%Y.%m.%d").date() == date
        ]
        
        if not date_lessons:
            await message.answer(f'{day} {month} занятий нет!', reply_markup=reply.keyboard_look)

            return
        
    except asyncio.TimeoutError:
            await message.answer("⚠️ Сервер ЮГУ не отвечает, попробуйте позже")
            return

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚠️ Ошибка при получении расписания:\n<code>{e}</code>",
            parse_mode="HTML"
        )
        await message.answer("⚠️ Не удалось получить расписание, попробуйте позже")
        return
    
    user = common_func.user_configs.get(user_id, {}).get('who')
    group_name, facultyOid = common_func.get_group_name(message, group_id) # Получаем имя группы или преподавателя и номер факультета
    
    user_theme = common_func.user_configs.get(user_id, {}).get('theme')

    if user == 'teacher':
        text_shedule = f'📅Расписание на {day} {month}, {weekday} \n{group_name}\n'
    else:
        text_shedule = f'📅Расписание на {day} {month}, {weekday} \nгруппа: {group_name}\n'
    
    for l in date_lessons:

        kind_of_work = l['kindOfWork']
        discipline = l['discipline']
        lesson_number = l['lessonNumberEnd'] 
        begin_lessson = l['beginLesson']
        end_lesson = l['endLesson']
        auditorium = l['auditorium']
        lecturer = l['lecturer_title']
        subgroup = l['subGroup']
        groups = l['stream']
        group = l['group']

        theme_func = theme.themes.get(user_theme, theme.themes.get('default'))
        
        text_shedule += theme_func(lesson_number,
                                    begin_lessson,
                                    end_lesson,
                                    auditorium,
                                    lecturer,
                                    discipline,
                                    kind_of_work,
                                    subgroup,
                                    user,
                                    groups,
                                    group,
                                    url_id)
        
    if user_theme == 'default':
         text_shedule += '————————————'
    
    await message.answer(text_shedule, parse_mode='HTML', reply_markup=reply.keyboard_look, disable_web_page_preview=True) # Отправляем расписание

    global request_counter # Cчетчк запросов
    request_counter += 1   
    
    common_func.save_hour_requests() # Запись в json
    common_func.last_request_time(message) # Запись времени последнего запроса в конфиг

    # Запись и сохранение логов
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    log_text = {
        'date_time': now_time,
        'username': message.from_user.username,
        'name': message.from_user.full_name,
        'id': message.from_user.id,
        'groupOid': group_id,
        'faculty_id': facultyOid,
        'group_name': group_name,
        'selected_date': f'{day} {month} {weekday}',
        'requests_count': request_counter
    }

    try:
        with open('logs.json', 'r', encoding='utf-8') as file:
            log_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_arr = []
    
    log_arr.append(log_text)
    
    with open('logs.json', 'w', encoding='utf-8') as logs_file:
        json.dump(log_arr, logs_file, ensure_ascii=False, indent=4)


async def shedule_by_date_link(message, date, day, month, weekday, user_id, command_args):

    if command_args and command_args.startswith('cab_'): # command.args --> cab_123
        request_object, cabinet_id = command_args.split('_') # request_object --> cab, cabinet_id --> 123

        url_id = f'auditoriumOid={cabinet_id}' # auditoriumOid=123

        group, auditorium_id = common_func.get_cabinet_info(None, int(url_id.replace('auditoriumOid=', '')))
        group_name = 'Кабинет: ' + group

    elif command_args and command_args.startswith('teacher_'):

        request_object, teacher_id = command_args.split('_') # request_object --> teacher, teacher_id --> 123

        url_id = f'lecturerOid={teacher_id}' # lecturerOid=123

        for t in teachers_file.teacher_file:
            if t ['lecturerOid'] == int(url_id.replace('lecturerOid=', '')):
                group_name = t['fio']
                    

    url = f'{API_BASE_URL}/lessons?fromdate={date}&todate={date}&{url_id}'

    try:
        async with message.bot.aiohttp_session.get(url) as response:
            if response.status != 200:
                await message.answer(f'⚠️ Ошибка сервера, попробуйте позже')
                return

            lessons_file = await response.json()
            lessons_sorted = sorted(lessons_file, key=lambda x: (datetime.strptime(x['date'], '%Y.%m.%d'), x['beginLesson']))

        date_lessons = [
            l for l in lessons_sorted
            if datetime.strptime(l["date"], "%Y.%m.%d").date() == date
        ]
        
        if not date_lessons:
            await message.answer(f'{day} {month} занятий нет!', reply_markup=reply.keyboard_look)

            return
        
    except asyncio.TimeoutError:
            await message.answer("⚠️ Сервер ЮГУ не отвечает, попробуйте позже")
            return

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚠️ Ошибка при получении расписания:\n<code>{e}</code>",
            parse_mode="HTML"
        )
        await message.answer("⚠️ Не удалось получить расписание, попробуйте позже")
        return
    
    user_theme = common_func.user_configs.get(user_id, {}).get('theme')

    text_shedule = f'📅Расписание на {day} {month}, {weekday} \n{group_name}\n'
    
    for l in date_lessons:

        kind_of_work = l['kindOfWork']
        discipline = l['discipline']
        lesson_number = l['lessonNumberEnd'] 
        begin_lessson = l['beginLesson']
        end_lesson = l['endLesson']
        auditorium = l['auditorium']
        lecturer = l['lecturer_title']
        subgroup = l['subGroup']
        groups = l['stream']
        group = l['group']

        theme_func = theme.themes.get(user_theme, theme.themes.get('default'))
        
        text_shedule += theme_func(lesson_number, 
                                   begin_lessson, 
                                   end_lesson,  
                                   auditorium, 
                                   lecturer, 
                                   discipline, 
                                   kind_of_work, 
                                   subgroup,
                                   None,
                                   groups, 
                                   group,
                                   request_object,
                                   url_id,
                                   )
        
    if user_theme == 'default':
         text_shedule += '————————————'
    
    await message.answer(text_shedule, parse_mode='HTML', reply_markup=reply.keyboard_look, disable_web_page_preview=True)

    global request_counter # Cчетчк запросов
    request_counter += 1   
    
    common_func.save_hour_requests() # Запись в json
    common_func.last_request_time(message) # Запись времени последнего запроса в конфиг

    # Запись и сохранение логов
    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    log_text = {
        'link_request': 1,
        'date_time': now_time,
        'username': message.from_user.username,
        'name': message.from_user.full_name,
        'id': message.from_user.id,
        'group_name': group_name,
        'selected_date': f'{day} {month} {weekday}',
        'requests_count': request_counter
    }

    try:
        with open('logs.json', 'r', encoding='utf-8') as file:
            log_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_arr = []
    
    log_arr.append(log_text)
    
    with open('logs.json', 'w', encoding='utf-8') as logs_file:
        json.dump(log_arr, logs_file, ensure_ascii=False, indent=4)