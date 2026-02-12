import asyncio
from aiogram import Bot, Dispatcher
import asyncio
from datetime import datetime
from aiogram.types import FSInputFile
from datetime import datetime
import os
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp

from handlers import commands
from callbacks import callback
from callbacks.callback import DisableBotMiddleware
from functions import async_func
from middleware.antispam import AntiSpamMiddleware

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

async def main():
    bot = Bot(BOT_TOKEN)
    #dp = Dispatcher()
    
    async def send_logs():
        
        while True:
            try:
                now_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
                

                file = FSInputFile('logs.json')
                caption = f'Логи бота за {now_time}, requests - {async_func.request_counter}'

                await bot.send_document(
                    chat_id=ADMIN_ID,
                    document=file,
                    caption=caption
                )

                print(f'[LOGS] Отправлены успешно в {now_time}')

            except Exception as e:
                print(f'[LOGS ERROR] Ошибка при отправке логов: {e}')

            await asyncio.sleep(3600)

    aiohttp_session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=15),
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://itport.ugrasu.ru",
            "Referer": "https://itport.ugrasu.ru/",
        }
    )

    bot.aiohttp_session = aiohttp_session
    print('Сессия запущена')
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(commands.BanMiddleware())
    dp.callback_query.middleware(commands.BanMiddleware())

    dp.message.middleware(AntiSpamMiddleware(max_messages=4, time_window=10))  # Подключение анти-спама 
    dp.message.middleware(DisableBotMiddleware())
    dp.callback_query.middleware(DisableBotMiddleware())

    dp.include_routers(commands.router, callback.router)
    asyncio.create_task(send_logs())

    try:
        await dp.start_polling(bot)
    finally:
        if not bot.session.closed:
            await bot.session.close()
            print('Сессия закрыта')

if __name__ == '__main__':
    asyncio.run(main()) 