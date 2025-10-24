import os
import json
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
    full_name = full_name.split()
    surname = full_name[0]
    name = full_name[1][0]
    mid_name = full_name[2][0]

    text = f'{surname} {name}.{mid_name}'

    return text
