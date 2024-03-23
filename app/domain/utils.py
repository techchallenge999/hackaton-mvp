import datetime


def get_current_month_first_days():
    now = datetime.datetime.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return first_day


def get_last_month_first_days():
    first_day = get_current_month_first_days()
    last_month_last_day = first_day - datetime.timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)
    return last_month_first_day


def get_today_first_time():
    now = datetime.datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return today


def get_tomorrow_first_time():
    now = datetime.datetime.now()
    tomorrow = now.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(days=1)
    return tomorrow
