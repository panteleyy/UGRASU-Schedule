from aiogram import types

kb_look = [
    [
        types.KeyboardButton(text='Расписание на сегодня'),
        types.KeyboardButton(text='Расписание на завтра')
    ],
    [
        types.KeyboardButton(text='Выбрать дату')
    ]
]
keyboard_look = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_look, input_field_placeholder='@panteleeyy')