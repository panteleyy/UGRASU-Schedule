from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from shedule_themes import theme
from dictionary import const_dictionary


def themes_keyboard():
    buttons = []
    for theme_name in theme.themes.keys():
        buttons.append([InlineKeyboardButton(text=const_dictionary.FULL_THEMES_NAMES.get(theme_name), callback_data=f'theme_{theme_name}')])
    theme_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return theme_keyboard