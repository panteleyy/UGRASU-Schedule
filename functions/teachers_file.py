import requests
from dotenv import load_dotenv
import os

from functions import common_func

load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

url = f'{API_BASE_URL}/lecturers'
#print(url)

headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.ugrasu.ru/",
            "Origin": "https://www.ugrasu.ru"
    }

response = requests.get(url, headers=headers)
teacher_file = response.json()

teachers = []
for t in teacher_file:
    fio = t.get('fio')
    if fio:
        short_name = common_func.short_name(fio)
        teachers.append(short_name.replace('.', ' ').lower().strip())
    else:
        teachers.append(None)

    #print(short_name)  

def get_teacheroid(name):
    name = name.lower().strip()  

    for t in teacher_file:
        short_name = common_func.short_name(t['fio'])
        short_name_clean = short_name.replace('.', ' ').lower().strip()

        if short_name_clean == name:
            return t['lecturerOid']

    return None

def get_teacher_id(name):
    for t in teacher_file:
        if name == t['shortFIO']:
            return t['lecturerOid']
    return None

