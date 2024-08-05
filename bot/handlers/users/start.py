from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

import asyncpg
from data import config

from loader import dp, db

from keyboards.default.my_qr_keybs import my_qr_codes

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await db.add_user(
            full_name=message.from_user.full_name,
            user_id=message.from_user.id,
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.get_user(user_id=message.from_user.id)
    text = f"Salom, {message.from_user.full_name}.\n\nQr code olish uchun /qr_code komandasini yuboring!"
    await message.answer(text, reply_markup=my_qr_codes)

