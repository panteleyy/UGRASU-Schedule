from functions import common_func
from dictionary import const_dictionary
from dotenv import load_dotenv
import os
import re


from functions import teachers_file, common_func

load_dotenv()
BOT_LINK = os.getenv('BOT_LINK')

def _is_linkable_aud(aud: str) -> bool:
        if not aud:
            return False
        if ' ' in aud:
            return False
        # if contains any Cyrillic letters -> do not link
        return re.search(r'[А-Яа-яЁё]', aud) is None

def short_kndwork(kind_of_work):
    return 'Практическое занятие' if kind_of_work == 'Практические (семинарские занятия)' else kind_of_work
    
def formate_lessons(discipline):
    return const_dictionary.SUBJECTS.get(discipline, discipline)

def default_theme(lesson_number, begin_lessson, end_lesson, auditorium, 
                  lecturer, discipline, kind_of_work, subgroup, user, 
                  groups,group, request_object, url_id=None
                  ):
    
    ### БАЗОВЫЙ ВЫВОД НА ЛЮБОЙ ЗАПРОС ###
    
    theme_text = "————————————\n" # ————————————
    theme_text += f'{common_func.find_emoji_number(kind_of_work, lesson_number)}<b>| {begin_lessson}-{end_lesson}</b>\n' # Пара1️⃣| 08:15-09:50
    theme_text += f"📚{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n" # 📚Физика - Практическое занятие

    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n" #🔹Подгруппа: 1

    ### ИМПОРТ ПАРАМЕТРОВ В ФУНКЦИИ ###

    ctx = {
        'auditorium': auditorium,
        'lecturer': lecturer,
        'groups': groups,
        'group': group,
        'subgroup': subgroup,
        'user': user
    }

    ### ВЫВОД ТЕМЫ ###  

    render = THEME_RENDERS.get(request_object, THEME_RENDERS['default'])

    theme_text += render(ctx)

    return theme_text

def render_cabinet_theme(ctx):

    theme_text = ''

    teacher_id = teachers_file.get_teacher_id(common_func.short_name(ctx['lecturer'])) 
    theme_text += f'<a href="{BOT_LINK}start=teacher_{teacher_id}">🎓{ctx["lecturer"]}</a>\n' # 🎓Препоадаватель Препоадаватель Препоадаватель 

    if ctx['groups'] is None:
           theme_text += f'👥Группа: {ctx["group"]}\n' # 👥Группа: 1111
    else:
        theme_text += f'👥Группы: {ctx["groups"]}\n' # 👥Группы: 1111 2222 3333

    return theme_text

def render_teacher_theme(ctx):
    
    theme_text = ''

    auditorium_name, auditorium_id = common_func.get_cabinet_info(ctx['auditorium'], None)

    if _is_linkable_aud(ctx['auditorium']) and auditorium_id: # 🏫3/351 
        theme_text += f'<a href="{BOT_LINK}start=cab_{auditorium_id}">🏫{ctx["auditorium"]}</a>\n'
    else:
        theme_text += f"🏫{ctx['auditorium']}\n"

    if ctx['groups'] is None:
        theme_text += f'👥Группа: {ctx["group"]}\n' # 👥Группа: 1111
    else:
        theme_text += f'👥Группы: {ctx["groups"]}\n' # 👥Группы: 1111 2222 3333

    return theme_text

def render_default_theme(ctx):

    theme_text = ''

    auditorium_name, auditorium_id = common_func.get_cabinet_info(ctx['auditorium'], None)

    if _is_linkable_aud(ctx['auditorium']) and auditorium_id: # 🏫3/351 
            theme_text += f'<a href="{BOT_LINK}start=cab_{auditorium_id}">🏫{ctx["auditorium"]}</a>\n'
    else:
        theme_text += f"🏫{ctx['auditorium']}\n"
        
    if ctx['user'] == 'student':
        teacher_id = teachers_file.get_teacher_id(common_func.short_name(ctx['lecturer'])) 
        theme_text += f'<a href="{BOT_LINK}start=teacher_{teacher_id}">🎓{ctx["lecturer"]}</a>\n' # 🎓Препоадаватель Препоадаватель Препоадаватель 
    else:
        if ctx['groups'] is None:
            theme_text += f'👥Группа: {ctx["group"]}\n' # 👥Группа: 1111
        else:
            theme_text += f'👥Группы: {ctx["groups"]}\n' # 👥Группы: 1111 2222 3333

    return theme_text

def old_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group, url_id=None):

    teacher_id = teachers_file.get_teacher_id(common_func.short_name(lecturer))

    theme_text = '\n'
    theme_text += f'📖{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"

    theme_text += f'🕰{begin_lessson} - {end_lesson}\n'

    if user == 'student':
        theme_text += f'[👤{lecturer}]({BOT_LINK}start=teacher_{teacher_id})\n'
    else:
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'

    theme_text += f'🚪{auditorium}\n'

    return theme_text

def standart_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group, url_id=None):
    teacher_id = teachers_file.get_teacher_id(common_func.short_name(lecturer))
    theme_text = '\n'
    theme_text += f'🕑{begin_lessson} - {end_lesson}\n'
    theme_text += f'📚{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'🏫{auditorium}\n'
    
    if user == 'student':
        theme_text += f'[👤{lecturer}]({BOT_LINK}start=teacher_{teacher_id})\n'
    else:
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'

    return theme_text

def marker_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group, url_id=None):
    teacher_id = teachers_file.get_teacher_id(common_func.short_name(lecturer))
    theme_text = '\n'
    theme_text += f'{const_dictionary.COLORED_KIND_OF_WORK.get(kind_of_work)} {formate_lessons(discipline)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'<b>•</b> {begin_lessson}-{end_lesson}\n'
    theme_text += f'<b>•</b> {auditorium}\n'

    if user == 'student':
        theme_text += f'<b>•</b> [{lecturer}]({BOT_LINK}start=teacher_{teacher_id})\n'
    else:
        if groups is None:
            theme_text += f'<b>•</b> Группа: {group}\n'
        else:
            theme_text += f'<b>•</b> Группы: {groups}\n'
    
    return theme_text

themes = {
    'default': default_theme,
    'old': old_theme,
    'standart': standart_theme,
    'marker': marker_theme
}

THEME_RENDERS = {
    'cab': render_cabinet_theme,
    'teacher': render_teacher_theme,
    'default': render_default_theme
}
