from aiogram import F
from aiogram.filters import CommandStart, Command

from handlers.user import (
    cmd_start, user_profile,
    referal_system, cmd_back_profile,
    cmd_static, cmd_bonus,
    cmd_check_plays, delete_check,
    add_balance_bot
)

from handlers.payment import (
    bay_bonus, check_payment
)

from handlers.game import game_start
from handlers.settings_play import win_mine, lose_mine, get_mines_prize

from loader_cfg import chat_id
from filters.chat_filter import ChatTypeFilter


class HandlersSetup:
    def __init__(self, dp):
        self.dp = dp

    async def setup_start(self):
        self.dp.message.register(
            cmd_start,
            CommandStart(),
            ChatTypeFilter('private')
        )

        self.dp.message.register(
            delete_check,
            Command("del")
        )

        self.dp.message.register(
            add_balance_bot,
            Command("add_balance")
        )

        self.dp.callback_query.register(
            user_profile,
            F.data.casefold().in_(['profile', 'back_ref'])
        )

        self.dp.channel_post.register(
            game_start,
            F.text, F.chat.id == chat_id
        )

        self.dp.callback_query.register(
            referal_system,
            F.data == 'ref'
        )

        self.dp.callback_query.register(
            cmd_back_profile,
            F.data == 'back'
        )

        self.dp.callback_query.register(
            cmd_static,
            F.data == 'static'
        )

        self.dp.callback_query.register(
            cmd_bonus,
            F.data.casefold().in_(['bonuss', 'back_bonus'])
        )

        self.dp.callback_query.register(
            bay_bonus,
            F.data.startswith('bonus_')
        )

        self.dp.callback_query.register(
            check_payment,
            F.data.startswith('check')
        )

        self.dp.callback_query.register(
            cmd_check_plays,
            F.data == 'plays'
        )

        self.dp.callback_query.register(
            win_mine,
            F.data.startswith('win_')
        )

        self.dp.callback_query.register(
            lose_mine,
            F.data.startswith('mines_')
        )

        self.dp.callback_query.register(
            get_mines_prize,
            F.data.startswith('save_')
        )