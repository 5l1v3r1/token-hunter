import datetime


def get_current(timezone):
    return datetime.datetime.now(timezone) \
        .strftime("%d/%m/%Y %H:%M:%S")
