from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

from shedule_themes import theme
from dictionary import const_dictionary


def themes_keyboard():
    buttons = []
    for theme_name in theme.themes.keys():
        buttons.append([InlineKeyboardButton(text=const_dictionary.FULL_THEMES_NAMES.get(theme_name), callback_data=f'theme_{theme_name}')])
    theme_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return theme_keyboard

def unban_user_keyboard():
    buttons = []

    try:
        with open('banned_users.json', 'r', encoding='utf-8') as file:
            banned_arr = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_arr = []

    for banned_user in banned_arr:
        buttons.append([InlineKeyboardButton(text=f'{banned_user}', callback_data=f'unban_{banned_user}')])
    
    unban_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return unban_keyboard

admin_keyboard_off = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📊 За месяц', callback_data='days_chart_bt'),
            InlineKeyboardButton(text='📊 Почасово', callback_data='hours_chart_bt'),
        ],
        [
            InlineKeyboardButton(text='📄 Логи', callback_data='logs_bt'),
            InlineKeyboardButton(text='⚙️ Конфиг', callback_data='config_bt'),
        ],
        [
            InlineKeyboardButton(text='🗓 Баны', callback_data='bans_bt'),
            InlineKeyboardButton(text='📋 Часы', callback_data='hours_bt'),
        ],
        [
            InlineKeyboardButton(text='⛔️ Бан', callback_data='ban_bt'),
            InlineKeyboardButton(text='✅ Разбан', callback_data='unban_bt'),
        ],
        [
            InlineKeyboardButton(text='🗑 Очистить логи', callback_data='clear_logs_bt'),
            InlineKeyboardButton(text='🗑 Очистить график', callback_data='clear_chart_bt'),
        ],
        [InlineKeyboardButton(text='🔴 Выключить бота', callback_data='disable_bot')],
    ]
)

admin_keyboard_on = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📊 За месяц', callback_data='days_chart_bt'),
            InlineKeyboardButton(text='📊 Почасово', callback_data='hours_chart_bt'),
        ],
        [
            InlineKeyboardButton(text='📄 Логи', callback_data='logs_bt'),
            InlineKeyboardButton(text='⚙️ Конфиг', callback_data='config_bt'),
        ],
        [
            InlineKeyboardButton(text='🗓 Баны', callback_data='bans_bt'),
            InlineKeyboardButton(text='📋 Часы', callback_data='hours_bt'),
        ],
        [
            InlineKeyboardButton(text='⛔️ Бан', callback_data='ban_bt'),
            InlineKeyboardButton(text='✅ Разбан', callback_data='unban_bt'),
        ],
        [
            InlineKeyboardButton(text='🗑 Очистить логи', callback_data='clear_logs_bt'),
            InlineKeyboardButton(text='🗑 Очистить график', callback_data='clear_chart_bt'),
        ],
        [InlineKeyboardButton(text='🟢 Включить бота', callback_data='enable_bot')],
    ]
)
  
chanel_ban_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_ban')]]
)


#moving_keyboard_buttons = InlineKeyboardMarkup(
#    inline_keyboard=[[InlineKeyboardButton(text='<', callback_data='previos_ver'), InlineKeyboardButton(text='>', callback_data='next_ver')]]
#)  