from aiogram import F
from aiogram.filters import CommandObject
from aiogram.types import Message, CallbackQuery

from keyboard.text import *
from signature import userdb, crypto
from keyboard.inline import UserKeyboard
from loader_cfg import erorr_users, ref_link, admin_ids


async def create_payment_error(amount, m, player_id, player_name):
    try:
        check = await crypto.create_check(asset='USDT', amount=amount)
        await m.bot.send_message(
            chat_id=player_id, text="💰", reply_markup=UserKeyboard.get_box(
                url=check.bot_check_url
            )
        )

    except Exception as e:
        print("error", e)
        erorr_users[player_name] = {"amount": amount}
        await m.bot.send_message(player_id, "У бота низкий баланс, подождите!")
        for admin in admin_ids:
            await m.bot.send_message(admin, 
                                     f"Ошибка для пользователя: {player_name}\n"
                                     f"<b>Слишком маленький баланс на счету бота!</b>")


async def cmd_start(m: Message, command: CommandObject):
    args = command.args
    user_id = m.from_user.id
    name = m.from_user.full_name

    await userdb.check_user(user_id=user_id, name=name)

    if args:
        if args == 'start':
            if not user_id in erorr_users:
                await m.answer("У вас нет чеков!")
            else:
                error_data = erorr_users[user_id]
                del erorr_users[user_id]
                await create_payment_error(amount=error_data["amount"], player_id=user_id, m=m,
                                    player_name=name)

        elif int(args) != m.from_user.id:
            if await userdb.check_user_referrer(user_id=user_id, referrer_id=int(args), name=name):
                try:
                    await m.bot.send_message(args, f"По вашей ссылке перешел рефер")
                except:
                    pass
            else:
                await m.answer(f"Вы являетесь реферером пользователя")
        else:
            await m.answer("Нельзя регистрироваться по своей же ссылке!")

    else:
        user_url = f'https://t.me/{m.from_user.username}'

        await m.answer(
            f"Привет, <b><a href='{user_url}'>{name}</a></b>!\n"
            f"Я бот для казино, мое имя AstralDep!\n\n",
            reply_markup=UserKeyboard.user_menu(),
            disable_web_page_preview=True
        )


async def user_profile(call: CallbackQuery):
    res = await userdb.get_user(user_id=call.from_user.id)
    msg = await text_profile(res=res, user_id=call.from_user.id, name=call.from_user.full_name)
    await call.message.edit_text(text=msg, reply_markup=UserKeyboard.user_ref_menu())


async def cmd_back_profile(call: CallbackQuery):
    await call.message.edit_text(
        f"Привет, <b><a href='https://t.me/{call.from_user.username}'>{call.from_user.first_name}</a></b>!\n"
        f"Я бот для казино, мое имя AstralDep!\n\n",
        reply_markup=UserKeyboard.user_menu(),
        disable_web_page_preview=True
    )


async def referal_system(call: CallbackQuery):
    ref_link_user = ref_link.format(user_id=call.from_user.id)
    await call.message.edit_text(
        f"Реферальная система, за каждую ставку нового пользовтеля от вас вы получаете 0.2% от его ставки\n\n"
        f"Ваша реферальная ссылка:\n"
        f"{ref_link_user}", reply_markup=UserKeyboard.back_referal()
    )


async def cmd_static(call: CallbackQuery):
    res, users_count = await userdb.get_statistic()

    await call.message.edit_text(
        f"<u><b>Статистика:</b></u>\n\n"
        f"<b>Сумма ставок:</b> {res.all_dep}$\n"
        f"<b>Выплат на сумму:</b> {res.all_pay}\n"
        f"<b>Пользователей в боте: {users_count}</b>", reply_markup=UserKeyboard.back_stat()
    )


async def cmd_bonus(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Выберите тариф который вам подходит:</b>", reply_markup=await UserKeyboard.get_bonus_menu()
    )


async def cmd_check_plays(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Актуальные игры в нашем боте:</b>", reply_markup=UserKeyboard.get_plays()
    )


async def delete_check(m: Message):
    checks = await crypto.get_checks()
    for check in checks:
        if check.status == 'active':    
            await crypto.delete_check(check_id=check.check_id)
    await m.answer("я удалил все чеки!")


async def add_balance_bot(m: Message, command: CommandObject):
    try:
        for ad_id in admin_ids:
            if m.from_user.id != ad_id:
                pass
            else:
                amount = int(command.args)
                link = await crypto.create_invoice(asset="USDT", amount=amount)
                await m.answer(f"{link.bot_invoice_url}")
    except:
        await m.answer("Указали неверно параметры, /add_balance 30")
