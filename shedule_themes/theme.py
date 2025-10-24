from functions import common_func
from dictionary import const_dictionary


def default_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_working, subgroup, is_last=False):
    theme_text = "————————————\n"
    theme_text += f"*Пара {lesson_number} | {begin_lessson}-{end_lesson}*\n"
    theme_text += f"📚{discipline} - {kind_of_working}\n"
    if subgroup != None:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f"🏫{auditorium}\n"
    theme_text += f"🎓{lecturer}\n"

    return theme_text
def old_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_working, subgroup):
    theme_text = '\n'
    theme_text += f'📖{discipline} - {kind_of_working}\n'
    if subgroup != None:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'🕰{begin_lessson} - {end_lesson}\n'
    theme_text += f'👤{lecturer}\n'
    theme_text += f'🚪{auditorium}\n'
    return theme_text

def standart_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_working, subgroup):
    theme_text = '\n'
    theme_text += f'🕑{begin_lessson} - {end_lesson}\n'
    theme_text += f'📚{discipline} - {kind_of_working}\n'
    if subgroup != None:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'🏫{auditorium}\n'
    theme_text += f'👤{common_func.short_name(lecturer)}\n'

    return theme_text

def marker_theme(lesson_number, begin_lessson, end_lesson, auditorium, lecturer, discipline, kind_of_working, subgroup, is_last=False):
    theme_text = '\n'
    theme_text += f'{const_dictionary.COLORED_KIND_OF_WORK.get(kind_of_working)} {discipline}\n'
    if subgroup != None:
        theme_text += f"🔹Подгруппа: {subgroup[-1]}\n"
    theme_text += f'*•* {begin_lessson}-{end_lesson}\n'
    theme_text += f'*•* {auditorium}\n'
    theme_text += f'*•* {common_func.short_name(lecturer)}\n'
    

    return theme_text

themes = {
    'default': default_theme,
    'old': old_theme,
    'standart': standart_theme,
    'marker': marker_theme
}

