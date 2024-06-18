import random
import asyncio

from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from signature import userdb, crypto
from keyboard.inline import UserKeyboard
from loader_cfg import (
    casino_chat, admin_ids, 
    erorr_users, numbers, mines_users
)
from keyboard.text import (
    win_message_cub, win_message_cnb,
    message_draw_cnb, win_message_mines,
    lose_message_mines, lose_message_cub,
    lose_message_cnb
)


async def create_payment(amount, m, player_id, player_name):
    try:
        check = await crypto.create_check(asset='USDT', amount=amount)

        await m.bot.send_message(
            chat_id=player_id, text="Заберите ваш выигрыш!", reply_markup=UserKeyboard.get_box(
                url=check.bot_check_url
            )
        )
        return 1
    except Exception as e:
        print("error", e)
        erorr_users[player_id] = {"amount": amount}
        for admin in admin_ids:
            await m.bot.send_message(admin, 
                                     f"Ошибка для пользователя: {player_name}\n"
                                     f"<b>Слишком маленький баланс на счету бота!</b>")
        return 0


async def get_rub():
    s = await crypto.get_exchange_rates()
    desired_rate = None
    for rate in s:
        if rate.source == 'USDT' and rate.target == 'RUB':
            desired_rate = rate
            return desired_rate


async def dice_play(player_id, player_name, bet_usdt,
                     values, percent, bonus, comment_play, m):
    x = await m.bot.send_dice(chat_id=casino_chat)

    num = x.dice.value
    win = 0
    desired_rate = await get_rub()

    if num == values or (isinstance(values, (list, tuple, set)) and num in values):
        win = 1
        sum_user = bet_usdt * percent
        res = await create_payment(m=m, player_id=player_id, player_name=player_name, amount=bet_usdt)
        win_message = await win_message_cub(player_name=player_name, bonus_status=bonus,
                                            sum_win=sum_user, rub=round(desired_rate.rate * bet_usdt, 2),
                                            comment="куб", comment_play=comment_play, value=num, status=res)

        keyboard = UserKeyboard.create_link() if res != 0 else UserKeyboard.back_user_money()
        await m.bot.send_message(
            chat_id=casino_chat,
            text=win_message,
            reply_markup=keyboard
            )
        
    else:
        lose_msg = await lose_message_cub(player_name=player_name, bonus_status=bonus, value=num)

        await m.bot.send_message(
            chat_id=casino_chat,
            text=lose_msg,
            reply_markup=UserKeyboard.create_link()
            )
    
    await userdb.add_user_bet(user_id=player_id, name=player_name,
                               money_ref=0, all_play=1, all_money=bet_usdt, count_vin=win)


async def cnb_play(player_id, player_name, bet_usdt,
                     values, percent, bonus, comment_play, m):
    win = 0
    desired_rate = await get_rub()

    bot_cnb = ["камень", "ножницы", "бумага"]

    cnb =  {
        "ножницы": "✌️",
        "камень": "✊",
        "бумага": "✋"
    }

    win_cnb = [
        ("ножницы", "бумага"),
        ("бумага", "камень"),
        ("камень", "ножницы")
    ]

    user_bet = cnb[comment_play]
    bot_value = random.choice(bot_cnb)
    bot_bet = values[bot_value]

    await m.bot.send_message(chat_id=casino_chat, text=f"{user_bet}")
    await m.bot.send_message(chat_id=casino_chat, text=f"{bot_bet}")

    if (comment_play, bot_value) in win_cnb:
        sum_user = bet_usdt * percent
        res = await create_payment(m=m, player_id=player_id, player_name=player_name, amount=bet_usdt)
        win_message = await win_message_cnb(player_name=player_name, bonus_status=bonus,
                                            sum_win=sum_user, rub=round(desired_rate.rate * bet_usdt, 2),
                                            comment="Кнб", comment_play=comment_play, value=bot_value, status=res)

        keyboard = UserKeyboard.create_link() if res != 0 else UserKeyboard.back_user_money()
        await m.bot.send_message(
            chat_id=casino_chat,
            text=win_message,
            reply_markup=keyboard
            )
        
    elif comment_play == bot_value:
        sum_user = bet_usdt * 0.1
        amount = bet_usdt - sum_user
        res = await create_payment(m=m, player_id=player_id, player_name=player_name, amount=amount)

        draw_message = await message_draw_cnb(player_name=player_name, bonus_status=bonus,
                                            sum_win=bet_usdt, rub=round(desired_rate.rate * bet_usdt, 2),
                                            comment="Кнб", comment_play=comment_play, value=bot_value, status=res)
        
        keyboard = UserKeyboard.create_link() if res != 0 else UserKeyboard.back_user_money()
        await m.bot.send_message(chat_id=casino_chat, text=draw_message, reply_markup=keyboard)
        
    else:
        lose_msg = await lose_message_cnb(player_name=player_name, bonus_status=bonus, value=bot_value)

        await m.bot.send_message(
            chat_id=casino_chat,
            text=lose_msg,
            reply_markup=UserKeyboard.create_link()
            )
    
    await userdb.add_user_bet(user_id=player_id, name=player_name,
                               money_ref=0, all_play=1, all_money=bet_usdt, count_vin=win)
    

async def mines_play(m, player_id, user_bet):
    mines_users[player_id] = {"level": 1, "amount": user_bet, "win_amount": user_bet}
    await m.bot.send_message(chat_id=casino_chat, text=(
        f"Начальная ставка: <b>{user_bet}</b>💲\n\n"
        f"<blockquote><b>1️⃣0.1x 2️⃣0.2x 3️⃣0.4x 4️⃣0.6x 5️⃣0.8x 6️⃣1x 7️⃣1.5x</b></blockquote>"
    ), 
                             reply_markup=UserKeyboard.get_create_mines(player_id=player_id, user_bet=user_bet))


async def win_mine(call: CallbackQuery):
    user_id = call.from_user.id
    level, player_id = call.data.split("_")[1], call.data.split("_")[2]

    x = numbers['мины']["values"][level]
    level_mines = mines_users[int(player_id)]["level"]
    user_bet = mines_users[int(player_id)]["amount"]
    win_amount = mines_users[int(player_id)]["win_amount"]

    if user_id != int(player_id):
        await call.answer("Это не ваша игра!")
    else:
        if int(level) != level_mines:
            await call.answer(f"Начните с {level_mines} уровня!")
        else:
            new_level = level_mines + 1
            new_percent = round(user_bet * x, 2)
            new_amount = round(win_amount + new_percent, 2)
            mines_users[int(player_id)] = {"level": new_level, "amount": user_bet, "win_amount": new_amount}

            inline_keyboard = call.message.reply_markup.inline_keyboard
            for row in inline_keyboard:
                for button in row:
                    if button.callback_data == call.data:
                        button.text = f"💰{x}x"
                        button.callback_data = "winner"
                    if button.callback_data.startswith("save_"):
                        button.text = f"Забрать {new_amount}💲"
                        button.callback_data = f"save_{player_id}_{new_amount}"

            await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))


async def lose_mine(call: CallbackQuery):
    user_id = call.from_user.id
    player_id, level = call.data.split("_")[1], call.data.split("_")[2]
    level_mines = mines_users[int(player_id)]["level"]

    if user_id != int(player_id):
        await call.answer("Это не ваша игра!")

    elif int(level) != level_mines:
            await call.answer(f"Начните с {level_mines} уровня!")
    else:
        inline_keyboard = call.message.reply_markup.inline_keyboard
        for row in inline_keyboard:
            for button in row:
                if button.callback_data == call.data:
                        button.text = "💥"
                        button.callback_data = f"lose"
                if button.callback_data.startswith("mines_"):
                    button.text = "💣"
                if button.callback_data.startswith("win_"):
                    button.text = '💎'
                button.callback_data = f"lose"
        await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))

        percent_bonus = await userdb.get_user_bonus_percent(user_id=int(player_id))
        bonus = '💎' if percent_bonus else ''
        msg_lose = await lose_message_mines(player_name=call.from_user.full_name, bonus_status=bonus)
        await call.message.bot.send_message(chat_id=casino_chat, text=msg_lose,
                                             reply_markup=UserKeyboard.create_link())


async def get_mines_prize(call: CallbackQuery):
    user_id = call.from_user.id
    player_id, prize = call.data.split("_")[1], call.data.split("_")[2]
    desired_rate = await get_rub()
    level_mines = mines_users[int(player_id)]["level"]

    if user_id != int(player_id):
        await call.answer("Это не ваша игра!")
    elif level_mines < 2:
        await call.answer("Откройте хотя бы один уровень!")
    else:
        del mines_users[int(player_id)]
        
        inline_keyboard = call.message.reply_markup.inline_keyboard
        for row in inline_keyboard:
            for button in row:
                if button.callback_data.startswith("mines_"):
                        button.text = "💣"
                if button.callback_data.startswith("win_"):
                    button.text = '💎'
                if button.callback_data.startswith("save_"):
                    button.text = f"💸Получено {float(prize)}💲"
                button.callback_data = f"lose"
        await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))

        res = await create_payment(player_id=int(player_id), amount=float(prize),
                                   m=call.message, player_name=call.from_user.full_name)
        percent_bonus = await userdb.get_user_bonus_percent(user_id=int(player_id))
        bonus = '💎' if percent_bonus else ''
        
        keyboard = UserKeyboard.create_link() if res != 0 else UserKeyboard.back_user_money()
        msg = await win_message_mines(player_name=call.from_user.full_name, bonus_status=bonus,
                                      sum_win=float(prize), rub=round(float(prize) * desired_rate.rate, 2),
                                      status=res)
        
        await call.message.bot.send_message(chat_id=casino_chat, text=msg, reply_markup=keyboard)

