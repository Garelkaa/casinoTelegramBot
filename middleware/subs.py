from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Dict, Callable

from keyboard.inline import UserKeyboard


class CheckSub(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        
        if event.chat.type == 'private':
            chat_member = await event.bot.get_chat_member(chat_id=-1002012049957, user_id=event.from_user.id)
            if chat_member.status == 'left':
                await event.answer(
                    f"✅Для использования бота, вы должны быть подписаны на канал:", reply_markup=UserKeyboard.check_subs()
                )
            else:
                return await handler(event, data)
        else:
            return await handler(event, data)
        