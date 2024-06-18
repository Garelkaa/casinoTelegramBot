from aiogram.types import Message

from loader_cfg import (
    numbers, casino_chat, erorr_users
)
from signature import userdb
from keyboard.inline import UserKeyboard
from keyboard.text import dep_message, dep_message_mines
from handlers.settings_play import dice_play, cnb_play, mines_play


async def game_start(m: Message):
    try:
        bet_usd = float(m.text.split("($")[1].split(").")[0])
        bet_comment = m.text.split("💬 ")[1].lower() if m.text.split("💬 ")[1:] else None
        player_name = m.text.split("отправил(а)")[0].strip()
        user = m.entities[0].user
        user_id = user.id if user else None
        player_id = user_id if user_id else await userdb.get_user_ref(name=player_name)

    except Exception as e:
         print("произошла ошибка при получении данных пользователя:", e)
         erorr_users[player_name] = {"amount": bet_usd}
         await m.bot.send_message(
             casino_chat, f"Ошибка для пользователя: {player_name}",
             reply_markup=UserKeyboard.back_user_money())

    if bet_comment and player_id:
        percent_bonus = await userdb.get_user_bonus_percent(user_id=player_id)
        bonus = '💎' if percent_bonus else ''
        bonus_dep = round(bet_usd * percent_bonus, 2) if percent_bonus else bet_usd

        print(f"Ставка: {bet_usd}\nКоммент: {bet_comment}\nИмя: {player_name}\nаЙДИ: {player_id}")
        comment_parts = bet_comment.split()
        comment = comment_parts[0].strip()
        comment_play = comment_parts[1].strip() if len(comment_parts) > 1 else None
        print(comment)
        print(comment_play)

        if comment not in numbers:
            await m.bot.send_message(casino_chat, f"Ошибка для пользователя: {player_name}")
            print("error")
        else:

            if comment == 'куб':
                values = numbers[comment]["plays"][comment_play]
                if values:
                    percent_status = numbers[comment]["percent"][comment_play]
                    percent = await userdb.get_percent_cub_one(status=percent_status, play=comment)
                    bet_send = await dep_message(player_name, bonus, bonus_dep, comment, comment_play, percent)

                    await m.bot.send_message(chat_id=casino_chat, text=bet_send, reply_markup=UserKeyboard.create_link())
                        
                    await dice_play(player_id=player_id, player_name=player_name, bet_usdt=bonus_dep,
                                    values=values, percent=percent, bonus=bonus,
                                    comment_play=comment_play, m=m)      

                else:
                    erorr_users[player_name] = {"amount": bet_usd}
                    await m.bot.send_message(
                        casino_chat, f"Ошибка для пользователя: {player_name}\nНеверно указана игра",
                        reply_markup=UserKeyboard.back_user_money()
                        )
                    print("error")

            elif comment in ['камень', 'ножницы', 'бумага']:
                values = numbers[comment]["plays"]
                if values:
                    percent_status = numbers[comment]["percent"]
                    percent = await userdb.get_percent_cub_one(status=percent_status, play=comment)
                    bet_send = await dep_message(player_name=player_name, bonus_status=bonus,
                                                bet_usd=bonus_dep, comment="Кнб",
                                                comment_play=comment, percent=percent)
                    
                    await m.bot.send_message(chat_id=casino_chat, text=bet_send, reply_markup=UserKeyboard.create_link())

                    await cnb_play(player_id=player_id, player_name=player_name, bet_usdt=bonus_dep,
                                    values=values, percent=percent, bonus=bonus,
                                    comment_play=comment, m=m)

                else:
                    erorr_users[player_name] = {"amount": bet_usd}
                    await m.bot.send_message(
                        casino_chat, f"Ошибка для пользователя: {player_name}\nНеверно указана игра",
                        reply_markup=UserKeyboard.back_user_money()
                        )
                    print("error")

            elif comment == 'мины':
                bet_send = await dep_message_mines(player_name=player_name, bonus_status=bonus,
                                                bet_usd=bonus_dep, comment="Мины")
                await m.bot.send_message(chat_id=casino_chat, text=bet_send, reply_markup=UserKeyboard.create_link())
                
                await mines_play(m=m, player_id=player_id, user_bet=bonus_dep)


            await userdb.add_user_ref_money(user_id=player_id, amount=bet_usd)
            await userdb.add_statistic(all_dep=bet_usd, all_pay=0)
            
    else:
        print("произошла ошибка при получении данных пользователя:")
        erorr_users[player_name] = {"amount": bet_usd}
        await m.bot.send_message(
            casino_chat, f"Ошибка для пользователя: {player_name}, у вас скрыт аккаунт! Напишите боту старт либо же откройте аккаунт!",
            reply_markup=UserKeyboard.back_user_money())
