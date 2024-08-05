from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext
import copy
import pytz


from uuid import uuid4
import qrcode
from environs import Env
import os

from data.config import ADMINS
from loader import dp, db

from tashkent_time import get_tashkent_time

from keyboards.inline.qr_inline_buttons import (
    active_qrs, working_qrs,
    activate_qr, before_finish_qr, finish_qr,
    qr_show_keyboard,
    qr_numb_keyboard,
    qr_finish_keyboard,
)


env = Env()
env.read_env()


tz_tashkent = pytz.timezone('Asia/Tashkent')

@dp.message_handler(Command('qr_code'), state='*')
async def qr_generate(message: types.Message, state: FSMContext):
    uid = str(uuid4())
    url = f"{env.str("SERVER_IP")}/{uid}"
    # url = f"{url}/{uid}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    image_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'site', "media"))
    name = f"{image_directory}/qrcode_{uid}.png"
    img.save(name)

    user = await db.get_user(message.from_user.id)
    qr = await db.add_qrcode(user[0], name, uid, True, False)
    with open(f"{image_directory}/qrcode_{uid}.png", 'rb') as photo:
        await message.answer_photo(photo)
    await message.reply(f"QR code raqami: {qr['id']}\n\nUsh bu qr code dan foydalanib taymerni faollashtiring")


async def menu_func(query, query_type=None):
    active_qr_count = await db.get_active_qrs_count(query.from_user.id)
    working_qr_count = await db.get_working_qrs_count(query.from_user.id)

    text = ""
    keyb = []
    if active_qr_count[0] > 0 and int(working_qr_count[0]) > 0:
        text += f"Sizda:\n<b>Aktiv: </b>{active_qr_count[0]}\n<b>Ishlayotgan: {working_qr_count[0]}</b>\nqr codelar mavjud."
        keyb = [1, 1]
    elif active_qr_count[0] > 0:
        keyb = [1, 0]
        text += f"Sizda {active_qr_count[0]} ta aktiv qr code mavjud."
    elif working_qr_count[0] > 0:
        keyb = [0, 1]
        text += f"Sizda {working_qr_count[0]} ta ishlayotgan qr code mavjud."
    else:
        keyb = [0, 0]
        text += f"Sizda qr code mavjud emas!\n\nQr code olish uchun /qr_code komandasini yuboring!"
    if keyb != [0, 0]:
        keyboards = await qr_show_keyboard(keyb)
    else:
        keyboards = None
    if query_type:
        await query.message.answer(text, reply_markup=keyboards)
    else:
        await query.answer(text, reply_markup=keyboards)


@dp.message_handler(text='QR kodlarim', state='*')
async def get_qr_codes(message: types.Message, state: FSMContext):
    await menu_func(message)

@dp.callback_query_handler(active_qrs.filter(), state='*')
async def active_qrs_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    qr_codes = await db.get_qrcodes(query.from_user.id)
    text = "<b>QR Code</b>ni aktivlashtirish uchun qr code raqami ustiga bosing!"
    keyboard = await qr_numb_keyboard(qr_codes, qr_type='activate')
    await query.message.delete()
    await query.message.answer(text=text, reply_markup=keyboard)

@dp.callback_query_handler(activate_qr.filter(), state='*')
async def activate_qrcode_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    qr_id = int(callback_data['id'])
    start_time = get_tashkent_time()
    is_success = None
    try:
        await db.activate_qr_code(qr_id=qr_id, start_time=start_time)
        price = await db.get_price()
        text = f"<b>{qr_id}</b> - qr code muvaffaqiyatli faollashtirildi.\n\n 1 soat foydalanish <b>narxi</b> -> <b>{price['price_per_hour']}</b>"
        is_success = True
    except Exception as e:
        text = "Tizimda nosozlik mavjud keyinroq urinib ko'ring:"
        text_admin = f"Qr codeni aktivlashtirishda xatolik mavjud: **QR Code id:** {qr_id}\n\n{e}"
        send_message_toadmin(text_admin)
    await query.message.delete()
    await query.message.answer(text=text)
    await menu_func(query, query_type='query')
    if is_success:
        send_message_toadmin(text)

@dp.callback_query_handler(working_qrs.filter(), state='*')
async def working_qrs_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    qr_codes = await db.get_working_qrcodes(query.from_user.id)
    text = "<b>QR Code</b>ni boshqarish uchun qr code raqami ustiga bosing!"
    keyboard = await qr_numb_keyboard(qr_codes, 'working')
    await query.message.delete()
    await query.message.answer(text=text, reply_markup=keyboard)

@dp.callback_query_handler(before_finish_qr.filter(), state='*')
async def before_finish_qrcode_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    qr_id = int(callback_data['id'])
    keyboard = None
    try:
        qr_code = await db.get_qrcode(query.from_user.id)
        price = await db.get_price()
        keyboard = await qr_finish_keyboard(qr_id)
        start_time = qr_code['start_time']
        start_time = start_time.astimezone(tz_tashkent)
        text = f"<b>QR Code:</b> {qr_id}\n<b>Faollashtilgan vaqti:</b> {str(start_time)[:16]}\n\n 1 soat foydalanish <b>narxi</b> -> <b>{price['price_per_hour']}</b>"
    except Exception as e:
        text_admin = f"Qr codeni yakunlashdan oldin xatolik mavjud: **QR Code id:** {qr_code['id']}\n\n{e}"
        send_message_toadmin(text_admin)
        text = "Tizimda nosozlik mavjud keyinroq urinib ko'ring:"
    await query.message.delete()
    await query.message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(finish_qr.filter(), state='*')
async def finish_qrcode_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    qr_id = int(callback_data['id'])
    current_time = get_tashkent_time()
    is_success = None
    try:
        qr_code = await db.get_qrcode(query.from_user.id)
        price = await db.get_price()
        start_time = qr_code['start_time']
        start_time = start_time.astimezone(tz_tashkent)
        cost = round(float((current_time - start_time).total_seconds()) / 3600 * float(price['price_per_hour']), 2)
        await db.finish_qr_code(current_time, cost, qr_id)
        text = f"""<b>QR Code:</b> {qr_id}
                    \n<b>Holati:</b> Yakunlangan
                    \n<b>Faollashtilgan vaqti:</b> {str(start_time)[:16]}
                    \n<b>Yakunlangan vaqti:</b> {str(current_time)[:16]}
                    \n<b>To'lov narxi:</b> {cost}
                    \n\n 1 soat foydalanish <b>narxi</b> -> <b>{price['price_per_hour']}</b>"""
        is_success = True
    except Exception as e:
        text_admin = f"Qr codeni yakunlashda xatolik mavjud: **QR Code id:** {qr_code['id']}\n\n{e}"
        send_message_toadmin(text_admin)
        text = "Tizimda nosozlik mavjud keyinroq urinib ko'ring:"
    await query.message.delete()
    await query.message.answer(text=text)   
    await menu_func(query, query_type='query')
    if is_success:
        send_message_toadmin(text)
        


async def send_message_toadmin(message):
    for admin in ADMINS:
        await dp.bot.send_message(admin, message)
