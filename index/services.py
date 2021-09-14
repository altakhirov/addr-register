from datetime import datetime


# `08.10.2020` => `2020-10-08`
def datetime_regex(dt):
    if dt:
        d = datetime.strptime(dt, '%d.%m.%Y')
        return d.strftime("%Y-%m-%d")
