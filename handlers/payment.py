from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboard.text import *
from signature import userdb, crypto
from keyboard.inline import UserKeyboard


async def bay_bonus(call: CallbackQuery, state: FSMContext):
    id = call.data.split("_")[1]
    res = await userdb.get_bonus(id=int(id))

    invoice = await crypto.create_invoice(asset='USDT', amount=res.price)
    await state.update_data(
        time=res.time,
        invoice=invoice,
        name=res.name_bonus,
        percent=res.percent
    )

    await call.message.edit_text(
        f"<b><u>Бонус</u></b> {res.name_bonus} №{id}\n\n"
        f"<b>Оипсание:</b> {res.description}\n\n"
        f"<b><u>Цена: {res.price}$</u></b>, <b><u>Время: {res.time} дней</u></b>",
          reply_markup=UserKeyboard.back_bonus(url=invoice.bot_invoice_url)
    )


async def check_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    invoice = data.get('invoice')

    invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)

    if invoices.status == 'paid':
        await userdb.update_bonus(user_id=call.from_user.id,
                                   time=data['time'], name_bonus=data['name'], percent=data['percent'])

        await call.message.edit_text(
            f"<b>Вы успешно оплатили!</b>\n\n"
            f"Теперь при каждой ставке вам будет начислен бонус!", reply_markup=UserKeyboard.payment_back()
        )
    else:
        await call.message.answer("Вы не оплатили счет!")