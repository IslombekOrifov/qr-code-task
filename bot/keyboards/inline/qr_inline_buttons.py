from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db


active_qrs = CallbackData("active_qrs", "all")
working_qrs = CallbackData("working_qrs", "all")

activate_qr = CallbackData("activate_qr", "id")
before_finish_qr = CallbackData("before_finish_qr", "id")
finish_qr = CallbackData("finish_qr", "id")
back = CallbackData("back", "all")

async def qr_show_keyboard(keyb):
    inlines = []
    if keyb[0] == 1:
        inlines.append(InlineKeyboardButton(
            text="Aktiv", callback_data=active_qrs.new(all='all')
        ))
    if keyb[1] == 1:
        inlines.append(InlineKeyboardButton(
            text="Ishlayotgan", callback_data=working_qrs.new(all='all')
        ))
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
       *inlines
    )
   
    return markup

async def qr_numb_keyboard(datas, qr_type):
    keyb = activate_qr
    if qr_type == 'working':
        keyb = before_finish_qr
    markup = InlineKeyboardMarkup(row_width=3)
    inlines = []
    for data in datas:
        data_id = data['id']
        inlines.append(InlineKeyboardButton(
            text=f"{data_id}", callback_data=keyb.new(id=f'{data_id}')
        ))
    markup.add(
       *inlines
    )
    return markup

async def qr_finish_keyboard(qr_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text=f"Yakunlash", callback_data=finish_qr.new(id=f'{qr_id}')
        ),
        InlineKeyboardButton(
            text=f"Orqaga", callback_data=back.new(all='all')
        ),
    )
    return markup