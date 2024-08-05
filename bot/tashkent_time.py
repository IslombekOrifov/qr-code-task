import pytz
import datetime

def get_tashkent_time():
    utc_now = datetime.datetime.now(pytz.utc)
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    tashkent_time = utc_now.astimezone(tashkent_tz)
    return tashkent_time