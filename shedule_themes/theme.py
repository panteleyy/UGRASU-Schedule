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

def default_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group, url_id=None):

    auditorium_name, auditorium_id = common_func.get_cabinet_info(auditorium, None)
    
    theme_text = "————————————\n"

    if kind_of_work == 'Практические (семинарские занятия)':
        theme_text += f"<b>Пара{const_dictionary.PRACTICAL_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    elif kind_of_work == 'Лекция':
        theme_text += f"<b>Пара{const_dictionary.LECTURE_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    elif kind_of_work == 'Пересдача экзамена' or kind_of_work == 'Экзамены':
        theme_text += f"<b>Пара{const_dictionary.EXAM_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    elif kind_of_work == 'Консультации перед экзаменом':
        theme_text += f"<b>Пара{const_dictionary.PREPARATION_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    elif kind_of_work == 'Пересдача дифференцированного зачета' or kind_of_work == 'Дифференцированный зачет':
        theme_text += f"<b>Пара{const_dictionary.DIFF_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    elif kind_of_work == 'Внеаудиторная ' or kind_of_work == 'Учебные практики (О)':
        theme_text += f"<b>Пара{const_dictionary.TALKING_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"
        
    elif kind_of_work == 'Лабораторные работы':
        theme_text += f"<b>Пара{const_dictionary.LAB_EMOJI.get(int(lesson_number))}| {begin_lessson}-{end_lesson}</b>\n"

    else:
        theme_text += f"<b>Пара {lesson_number} | {begin_lessson}-{end_lesson}</b>\n"
    theme_text += f"📚{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n"
    
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    
    if _is_linkable_aud(auditorium) and auditorium_id:
        theme_text += f'<a href="{BOT_LINK}start=cab_{auditorium_id}">🏫{auditorium}</a>\n'
    else:
        theme_text += f"🏫{auditorium}\n"
    
    if user == 'student':
        teacher_id = teachers_file.get_teacher_id(common_func.short_name(lecturer))
        theme_text += f'<a href="{BOT_LINK}start=teacher_{teacher_id}">🎓{lecturer}</a>\n'
    else:
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'
    
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
    theme_text += f'*•* {begin_lessson}-{end_lesson}\n'
    theme_text += f'*•* {auditorium}\n'

    if user == 'student':
        theme_text += f'*•* [{lecturer}]({BOT_LINK}start=teacher_{teacher_id})\n'
    else:
        if groups is None:
            theme_text += f'*•* Группа: {group}\n'
        else:
            theme_text += f'*•* Группы: {groups}\n'
    
    return theme_text

themes = {
    'default': default_theme,
    'old': old_theme,
    'standart': standart_theme,
    'marker': marker_theme
}

