from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import UserQrCode, Pricing
from .bot import send_bot_message

from environs import Env

import markdown

env = Env()
env.read_env()


ADMINS = env.list("ADMINS")


def index(request, uid):
    qr_code = UserQrCode.objects.filter(uid=uid, is_active=True).last()
    if qr_code:
        price = Pricing.objects.last()
        qr_code.is_active = False
        current_time = timezone.now()
        qr_code.start_time = current_time
        qr_code.save()
        user_text = f"Qr code [{qr_code.id}] muvaffaqiyatli faollashtirildi.\n**1 soat foydalanish qiymati: {price.price_per_hour}**"
        admin_text = f"Qr code [{qr_code.id}] faollashtirildi.\n**1 soat foydalanish qiymati: {price.price_per_hour}**\nuser-id: {qr_code.user.user_id}"

        send_bot_message(user_text, qr_code.user.user_id)
        for admin in ADMINS:
            send_bot_message(admin_text, admin)
    else:    
        user_text = f"Qr code faollashtirilgan. Yoki mavjud emas."
    user_text =  markdown.markdown(user_text)
    return render(request, 'main/index.html', {'user_text': user_text})
