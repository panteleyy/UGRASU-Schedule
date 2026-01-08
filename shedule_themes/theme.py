from functions import common_func
from dictionary import const_dictionary


def short_kndwork(kind_of_work):
    return 'Практическое занятие' if kind_of_work == 'Практические (семинарские занятия)' else kind_of_work
    
def formate_lessons(discipline):
    return const_dictionary.SUBJECTS.get(discipline, discipline)

def default_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group):
    theme_text = "————————————\n"
    theme_text += f"*Пара {lesson_number} | {begin_lessson}-{end_lesson}*\n"
    theme_text += f"📚{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n"

    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"

    theme_text += f"🏫{auditorium}\n"

    if user == 'teacher':
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'
    if user == 'student':
        theme_text += f'🎓{lecturer}\n'

    return theme_text
def old_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group):
    theme_text = '\n'
    theme_text += f'📖{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'🕰{begin_lessson} - {end_lesson}\n'
    if user == 'student':
        theme_text += f'👤{lecturer}\n'
    theme_text += f'🚪{auditorium}\n'
    if user == 'teacher':
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'
    return theme_text

def standart_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group):
    theme_text = '\n'
    theme_text += f'🕑{begin_lessson} - {end_lesson}\n'
    theme_text += f'📚{formate_lessons(discipline)} - {short_kndwork(kind_of_work)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'🏫{auditorium}\n'
    if user == 'teacher':
        if groups is None:
            theme_text += f'👥Группа: {group}\n'
        else:
            theme_text += f'👥Группы: {groups}\n'
    if user == 'student':
        theme_text += f'👤{common_func.short_name(lecturer)}\n'

    return theme_text

def marker_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_work, subgroup, user, groups, group):
    theme_text = '\n'
    theme_text += f'{const_dictionary.COLORED_KIND_OF_WORK.get(kind_of_work)} {formate_lessons(discipline)}\n'
    if subgroup:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'*•* {begin_lessson}-{end_lesson}\n'
    theme_text += f'*•* {auditorium}\n'
    if user == 'teacher':
        if groups is None:
            theme_text += f'*•* Группа: {group}\n'
        else:
            theme_text += f'*•* Группы: {groups}\n'
    if user == 'student':
        theme_text += f'*•* {common_func.short_name(lecturer)}\n'
    
    return theme_text

themes = {
    'default': default_theme,
    'old': old_theme,
    'standart': standart_theme,
    'marker': marker_theme
}

