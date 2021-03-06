from main import bot, dp, anti_flood, user_db
from aiogram import types
from config import payments_token, cash

async def send_offer(user_id, price: int):
    await bot.send_invoice(user_id,
                           title='{} рублей'.format(price),
                           description='Пополнение баланса на {} рублей'.format(price),
                           provider_token=payments_token,
                           currency='RUB',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[types.LabeledPrice(label='{} рублей'.format(price), amount=price * 100)],
                           start_parameter='time-machine-example',
                           payload=price
                           )

@dp.message_handler(commands =['get_offer'])
@dp.throttled(anti_flood, rate=1)
async def get_offer(m: types.Message):
    user_id = m.from_user.id
    return await send_offer(user_id, cash)

#проверка нажатия - тру кнопки при пополнении
@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    return await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    invoice_payload = message.successful_payment.to_python()['invoice_payload']
    print(invoice_payload)
    user_db.update_cash(message.from_user.id, cash)
    return