import json
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from dictionary import const_dictionary
from functions import common_func
from keyboards import reply
from shedule_themes import theme

load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

request_counter = 0

async def shedule_by_date(message, date, day, month, weekday):
    user_id = str(message.from_user.id)
    group_id = common_func.user_configs.get(user_id, {}).get('group_id')

    user_data = common_func.user_configs.get(user_id, {})

    group_oid = user_data.get('group_id')
    if not group_oid:
        await message.answer('Сначала выбери группу с помощью /group, а лучше посмотри изменения новой версии /start')
        return
    

    url = f'{API_BASE_URL}/lessons?fromdate={date}&todate={date}&groupOid={group_id}'

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
        await message.answer(f'{day} {month} занятий нет!')
        return
    
    text_shedule = f'📅Расписание на {day} {month}, {weekday}\n'
    for l in date_lessons:

        kind_of_work = l['kindOfWork']
        if kind_of_work == 'Практические (семинарские занятия)':
            kind_of_working = 'Практическое занятие'
        else:  
            kind_of_working = kind_of_work

        discipline = l['discipline']
        if discipline in const_dictionary.SUBJECTS:
            discipline = const_dictionary.SUBJECTS[discipline]

        lesson_number = l['lessonNumberEnd'] 
        begin_lessson = l['beginLesson']
        end_lesson = l['endLesson']
        auditorium = l['auditorium']
        lecturer = l['lecturer_title']
        subgroup = l['subGroup']

        user_theme = common_func.user_configs.get(user_id, {}).get('theme')

        theme_func = theme.themes.get(user_theme)
        
        text_shedule += theme_func(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_working, subgroup)
        
    if user_theme == 'default':
            text_shedule += '————————————'
    await message.answer(text_shedule, parse_mode='Markdown', reply_markup=reply.keyboard_look)

    global request_counter
    request_counter += 1

    facultyOid = common_func.user_configs.get(user_id, {}).get('facultyOid')

    group_url = f'{API_BASE_URL}/groups?facultyOid={facultyOid}'

    group_headers = {'User-Agent': 'Mozilla/5.0'}
    group_r = requests.get(group_url, headers=group_headers)
    names = group_r.json()

    for name in names:
        if name['groupOid'] == group_id:
            group_name = name['name']

    now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

    log_text = {
        'date_time': now_time,
        'username': message.from_user.username,
        'name': message.from_user.full_name,
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
            


    
