from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Dict, Callable


class StateBot(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:

        status = 0
        if status == 1:
            await event.answer("Бот на тех исправлениях!")
        else:
            return await handler(event, data)