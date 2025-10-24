from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from functions import common_func
from keyboards import reply

router = Router()

@router.callback_query(F.data.startswith('faculty_'))
async def handle_faculty(callback: CallbackQuery):
    faculty_id = int(callback.data.split('_')[1])
    user_id = str(callback.from_user.id)

    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'facultyOid': faculty_id
    })

    common_func.save_configs(common_func.user_configs)

    await callback.answer()
    group_kb = common_func.find_groups(faculty_id)

    await callback.message.edit_text('Выбери группу:', reply_markup=group_kb)

@router.callback_query(F.data.startswith('group_'))
async def handle_group(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    group_id = int(callback.data.split('_')[1])

    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'group_id': group_id
    })

    common_func.save_configs(common_func.user_configs)

    await callback.answer()

    await callback.message.edit_text(f'Группа выбрана!')
    await callback.message.answer('Выбери действие:', reply_markup=reply.keyboard_look)
    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'theme': 'default'
    })

    common_func.save_configs(common_func.user_configs)

@router.callback_query(F.data.startswith('back_'))
async def handle_back_group(callback: CallbackQuery):
    await callback.message.edit_text('Выбери факультет:', reply_markup=common_func.find_faculties())

@router.callback_query(F.data.startswith('theme_'))
async def handle_themes(callback: CallbackQuery):
    theme_name = callback.data[len('theme_'):]
    user_id = str(callback.from_user.id)

    await callback.answer()
    
    if user_id not in common_func.user_configs:
        common_func.user_configs[user_id] = {}

    common_func.user_configs[user_id].update({
        'theme': theme_name
    })

    common_func.save_configs(common_func.user_configs)

    await callback.message.answer('Тема выбрана!')