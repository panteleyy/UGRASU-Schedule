from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, timedelta
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv('ADMIN_ID'))

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, max_messages: int = 3, time_window: int = 10):
        self.max_messages = max_messages
        self.time_window = time_window
        self.user_messages: Dict[int, list[datetime]] = {}
        self.lock = asyncio.Lock()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        # Исключение для админа
        #if user_id == ADMIN_ID:
            #return await handler(event, data)

        async with self.lock:
            now = datetime.now()
            timestamps = self.user_messages.get(user_id, [])

            
            timestamps = [t for t in timestamps if now - t <= timedelta(seconds=self.time_window)]
            
            if len(timestamps) >= self.max_messages:
                
                if len(timestamps) == self.max_messages:
                    await event.answer(
                        "🚫 Слишком быстро! Подождите 10 секунд перед следующим сообщением.",
                        show_alert=False
                    )
                
                return None  

            
            timestamps.append(now)
            self.user_messages[user_id] = timestamps

       
        return await handler(event, data)