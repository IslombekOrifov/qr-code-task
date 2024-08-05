import requests
from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

token = env.str("BOT_TOKEN")

url = f'https://api.telegram.org/bot{token}/sendMessage'

def send_bot_message(message, user):
    data = {
        "chat_id" : user,
        "text" : message,
        'parse_mode' : 'markdown'
    }
    requests.post(url=url, data=data)
    return 0