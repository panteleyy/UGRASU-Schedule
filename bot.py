import asyncio
from aiogram import Bot, Dispatcher
import asyncio
from datetime import datetime
from aiogram.types import FSInputFile
from datetime import datetime
import os
from dotenv import load_dotenv

from handlers import commands
from callbacks import callback
from functions import async_func
from middleware.antispam import AntiSpamMiddleware

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    
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

    dp.include_routers(
        commands.router,
        callback.router
    )

    dp.message.middleware(AntiSpamMiddleware(max_messages=5, time_window=10))  # Подключение анти-спама 

    asyncio.create_task(send_logs())
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main()) 