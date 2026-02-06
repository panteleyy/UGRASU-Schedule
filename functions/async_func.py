import json
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from datetime import datetime

from functions import common_func
from keyboards import reply
from shedule_themes import theme


load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

request_counter = 0

async def shedule_by_date(message, date, day, month, weekday, user_id, url_id):

    group_id = common_func.user_configs.get(user_id, {}).get('group_id') # Получаем айди выбранной группы или преподавателя

    if not group_id: # Проверка на наличе группы
        await message.answer('Сначала выбери группу /group или преподавателя /teacher, а лучше посмотри изменения новой версии /changelog')
        return
    
    url = f'{API_BASE_URL}/lessons?fromdate={date}&todate={date}&{url_id}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://itport.ugrasu.ru",
        "Referer": "https://itport.ugrasu.ru/",
    }
    response = requests.get(url, headers=headers)
    lessons_file = response.json()
    lessons_sorted = sorted(lessons_file, key=lambda x: (datetime.strptime(x['date'], '%Y.%m.%d'), x['beginLesson']))

    date_lessons = [
        l for l in lessons_sorted
        if datetime.strptime(l["date"], "%Y.%m.%d").date() == date
    ]
    
    if not date_lessons:
        await message.answer(f'{day} {month} занятий нет!', reply_markup=reply.keyboard_look)

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

        theme_func = theme.themes.get(user_theme)
        
        text_shedule += theme_func(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group)
        
    if user_theme == 'default':
         text_shedule += '————————————'
    
    await message.answer(text_shedule, parse_mode='Markdown', reply_markup=reply.keyboard_look) # Отправляем расписание

    global request_counter # Cчетчк запросов
    request_counter += 1   
    
    common_func.save_hour_requests() # Запись в json
    common_func.save_day_requests() 

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