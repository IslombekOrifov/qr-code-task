from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


my_qr_codes = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='QR kodlarim',),
        ],
    ],
    resize_keyboard=True,
)