import random

from loader_cfg import random_lose_mes

async def text_profile(res, user_id, name):
    bonus = f'<i>{res.name_bonus}</i> на <b>{res.time}</b> дней' if res.bonus != 'Отсутствует' else res.bonus
    
    msg = (
        f"<u><b>Твой профиль:</b></u>\n\n"
        f"<b>ID:</b> <code>{user_id}</code>\n"
        f"<b>Имя:</b> <code>{name}</code>\n"
        f"<b>Успешных ставок:</b> {res.count_vin}\n"
        f"<b>Всего ставок:</b> {res.all_play} на {round(res.all_money, 2)}$\n"
        f"<b>Реф. баланс:</b> {round(res.money_ref, 2)}$\n"
        f"<b>Ваш бонус:</b> {bonus}"
    )
    return msg


async def dep_message(player_name, bonus_status, bet_usd, comment, comment_play, percent):
    bonus_mes = "\n<b><blockquote>У игрока есть бонус💎, его ставка умножена  на 0.5!</blockquote></b>\n\n" if bonus_status == '💎' else "\n\n"

    msg = (
            f"🎉<b>Принята новая ставка от</b> <b>[{player_name}{bonus_status}]</b>, <b>пожелаем ему удачи!</b>\n\n"
            f"<blockquote>💵 Поставил: <b>{bet_usd} 💲</b></blockquote>\n"
            f"<blockquote>🎮Игра: <b>{comment}</b> | 🗨️Ставка: <b>{comment_play}</b> | 📈Кэф: <b>{percent}</b></blockquote>"
            f"{bonus_mes}"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    
    return msg


async def win_message_cub(player_name, bonus_status, sum_win,
                            rub, comment, comment_play, value, status):
    winner = f"<blockquote><b>Выигрыш отправлен игроку {player_name}{bonus_status}!</b></blockquote>" if status == 1 else f"<blockquote><b>{player_name}{bonus_status}, заберите ваш выигрыш!</b></blockquote>"
    msg = (
            f"💰<b>Победа, выпало число {value}!</b>\n\n"
            f"<blockquote>💸 Выигрыш: <b>{sum_win} 💲 ({rub} RUB)</b></blockquote>\n"
            f"<blockquote>🎮 Игра: <b>{comment}</b> | 🗨️Ставка: <b>{comment_play}</b></blockquote>\n"
            f"{winner}\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    return msg


async def win_message_cnb(player_name, bonus_status, sum_win,
                            rub, comment, comment_play, value, status):
    winner = f"<blockquote><b>Выигрыш отправлен игроку {player_name}{bonus_status}!</b></blockquote>" if status == 1 else f"<blockquote><b>{player_name}{bonus_status}, заберите ваш выигрыш!</b></blockquote>"
    value = 'бумагу' if value == 'бумага' else value

    msg = (
            f"💰<b>Победа, бот поставил {value}!</b>\n\n"
            f"<blockquote>💸 Выигрыш: <b>{sum_win} 💲 ({rub} RUB)</b></blockquote>\n"
            f"<blockquote>🎮 Игра: <b>{comment}</b> | 🗨️Ставка: <b>{comment_play}</b></blockquote>\n"
            f"{winner}\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    return msg


async def message_draw_cnb(player_name, bonus_status, sum_win,
                            rub, comment, comment_play, value, status):
    winner = f"<blockquote><b>Ставка отправлена игроку {player_name}{bonus_status} с комиссией 10%.</b></blockquote>" if status == 1 else f"<blockquote><b>{player_name}{bonus_status}, заберите вашу ставку с комиссией 10%.</b></blockquote>"
    value = 'бумагу' if value == 'бумага' else value

    msg = (
            f"💰<b>Ничья, бот поставил {value}!</b>\n\n"
            f"<blockquote>💸 Cтавка: <b>{sum_win} 💲 ({rub} RUB)</b></blockquote>\n"
            f"<blockquote>🎮 Игра: <b>{comment}</b> | 🗨️Ставка: <b>{comment_play}</b></blockquote>\n"
            f"{winner}\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    return msg


async def win_message_mines(player_name, bonus_status, sum_win, rub, status):
    winner = f"<blockquote><b>Выигрыш отправлен игроку {player_name}{bonus_status}!</b></blockquote>" if status == 1 else f"<blockquote><b>{player_name}{bonus_status}, заберите ваш выигрыш!</b></blockquote>"

    msg = (
            f"💰<b>Пользователь забрал приз!</b>\n\n"
            f"<blockquote>💸 Выигрыш: <b>{sum_win} 💲 ({rub} RUB)</b></blockquote>\n"
            f"<blockquote>🎮 Игра: <b>Мины</b></blockquote>\n"
            f"{winner}\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    return msg


async def dep_message_mines(player_name, bonus_status, bet_usd, comment):
    bonus_mes = "\n<b><blockquote>У игрока есть бонус💎, его ставка умножена  на 0.5!</blockquote></b>\n\n" if bonus_status == '💎' else "\n\n"

    msg = (
            f"🎉<b>Принята новая ставка от</b> <b>[{player_name}{bonus_status}]</b>, <b>пожелаем ему удачи!</b>\n\n"
            f"<blockquote>💵 Поставил: <b>{bet_usd} 💲</b></blockquote>\n"
            f"<blockquote>🎮Игра: <b>{comment}</b> | 📈Кэф: <b>0.1x | 1.5x</b></blockquote>"
            f"{bonus_mes}"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    
    return msg


async def lose_message_mines(player_name, bonus_status):
    rnd_word = random.choice(random_lose_mes)

    msg = (
            f"<b>Поражение, {player_name}{bonus_status}, вы взорвались на мине!\n\n</b>"
            f"<blockquote>{rnd_word}</blockquote>\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    
    return msg


async def lose_message_cub(player_name, bonus_status, value):
    rnd_word = random.choice(random_lose_mes)

    msg = (
            f"<b>Поражение, {player_name}{bonus_status}, вы не угадали, выпало число {value}\n\n</b>"
            f"<blockquote>{rnd_word}</blockquote>\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    
    return msg


async def lose_message_cnb(player_name, bonus_status, value):
    value = 'бумагу' if value == 'бумага' else value
    rnd_word = random.choice(random_lose_mes)

    msg = (
            f"<b>Поражение, {player_name}{bonus_status}, вы не угадали, бот поставил {value}\n\n</b>"
            f"<blockquote>{rnd_word}</blockquote>\n\n"
            f"▫️Правила | Приобрести бонус | AstralDepBot▫️"
        )
    
    return msg
