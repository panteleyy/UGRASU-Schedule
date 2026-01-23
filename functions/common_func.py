import os
import json
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from dictionary import const_dictionary

load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

def load_configs():
    if os.path.exists(const_dictionary.CONFIG_FILE): 
        with open(const_dictionary.CONFIG_FILE, 'r', encoding='utf-8') as f: 
            return json.load(f)
    return {}
def save_configs(data):
    with open(const_dictionary.CONFIG_FILE, 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)
user_configs = load_configs()

def find_faculties():
    url = f'{API_BASE_URL}/faculties'
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    faculties_file = response.json()

    buttons = []
    rm_faculties = ['!Служебный', 'Филиалы ЮГУ', 'Югорский государственный университет', 'Элективные дисциплины по физической культуре и спорту']
    for facultiet in faculties_file:
        if facultiet['name'] not in rm_faculties:
            buttons.append([InlineKeyboardButton(text=facultiet['name'], callback_data=f'faculty_{facultiet['facultyOid']}')])

    faculkb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return faculkb

def find_groups(faculty_id: int):
    
    url = f'{API_BASE_URL}/groups?facultyOid={faculty_id}'

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    groups_file = response.json()

    buttons_storage = []
    buttons = []
    for group in groups_file:
        button = InlineKeyboardButton(
            text=group['name'],
            callback_data=f'group_{group['groupOid']}'
        )
        buttons_storage.append(button)
        if len(buttons_storage) == 3:
            buttons.append(buttons_storage)
            buttons_storage = [] 
    buttons.append([InlineKeyboardButton(text='Назад', callback_data='back_')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def dates_to_keyboard():
    kb_dates =[]
    kb_storage = []
    today_date = datetime.today().date()

    for offest in range(-8, 14-1):
        date = today_date + timedelta(days=offest)

        day = date.strftime('%d')
        day = str(int(day))
        month = const_dictionary.MONTHS[date.strftime('%m')]
        week = const_dictionary.WEEKDAYS[date.weekday()]

        text = f'{day} {month}, {week}'
        if offest == 0:
            text += '(Сегодня)'

        kb_storage.append(KeyboardButton(text=text))

        if len(kb_storage) == 2:
            kb_dates.append(kb_storage)
            kb_storage = []

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_dates, one_time_keyboard=True)

def text_to_date(date_str):
    day_part = date_str.split()[0]
    month_word = date_str.split()[1].strip(',')

    day = day_part.zfill(2)
    month = const_dictionary.REVERSED_MONTH.get(month_word)

    return day, month

def date_to_text(date_str):
    day = date_str.strftime('%d')
    day = str(int(day))

    month_part = date_str.strftime('%m')
    month = const_dictionary.MONTHS.get(month_part)

    return day, month   

def get_weekday(date_str):
    weekday_number = date_str.weekday()
    weekday = const_dictionary.WEEKDAYS.get(weekday_number)

    return weekday

def short_name(full_name):
    if not full_name:
        return 'Неизвестно'

    parts = full_name.split()

    if len(parts) >= 3:
        surname, name, mid_name = parts[0], parts[1], parts[2]
        return f'{surname} {name[0]}.{mid_name[0]}.'
    elif len(parts) == 2:
        surname, name = parts
        return f'{surname} {name[0]}.'
    else:
        return parts[0]


def get_group_name(message, group_id):
    from functions import teachers_file
    
    user_id = str(message.from_user.id)
    who = user_configs.get(user_id, {}).get("who")


    if who == "teacher":
        for t in teachers_file.teacher_file:
            if t["lecturerOid"] == group_id:
                teacher_name = t["fio"]
                return teacher_name, None
        return "Преподаватель", None
    
    facultyOid = user_configs.get(user_id, {}).get('facultyOid')

    group_url = f'{API_BASE_URL}/groups?facultyOid={facultyOid}'
    group_r = requests.get(group_url)
    names = group_r.json()

    if who == 'student':
       for name in names:
        if name['groupOid'] == group_id:
            return name['name'], facultyOid

def save_hour_requests():
    
    current_hour = datetime.now().strftime('%d.%m - %H') # Текущий час + дата

    try:
        with open('hour_requests.json', 'r', encoding='utf-8') as file:
            hour_requests = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        hour_requests = []

    for item in hour_requests:  # Если уже есть такая дата то добавить 1 запрос
        if item['date'] == current_hour:
            item['hour_requests'] += 1
            break    
    else: # Иначе добавить новый блок

        hour_requests.append(
            {
                'date': current_hour, 
                'hour_requests': 1 
            }
        )
    
    if len(hour_requests) > 24: # Учитывать только 24 
       hour_requests = hour_requests[-24:]


    with open('hour_requests.json', 'w', encoding='utf-8') as hour_requests_file:
        json.dump(hour_requests, hour_requests_file, ensure_ascii=False, indent=4)

def make_chart():

    with open("hour_requests.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    now_time = []
    hour_requests_counter = []

    for item in data: # Достаем данные из json и добавляем в массивы
        now_time.append(item['date'])
        hour_requests_counter.append(item['hour_requests'])

    plt.figure(figsize=(10, 5)) # Размеры графика

    #plt.grid(True)

    plt.bar(now_time, hour_requests_counter) # Что будет в графике
    plt.xticks(rotation=25) # Поворот подписей на 25 градусов

    plt.grid(axis='y', linestyle='--', alpha=0.7) # Cетка по x
    plt.grid(axis='x', linestyle='--', alpha=0.7) # Сетка по y

    for i in range(len(now_time)): # Количество запросов над каждым столбиком
        plt.text(i, hour_requests_counter[i], str(hour_requests_counter[i]), ha='center', va='bottom', fontsize=10)

    plt.title('Активность за последние часы') # Название графика
    plt.ylabel('Количество запросов') # Подпись y

    plt.savefig('chart.png') # Сохранение 
    plt.close() # Закрытие
    #plt.show()