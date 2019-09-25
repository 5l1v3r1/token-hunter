import datetime

def get_current_utc():
    return datetime.datetime.now(datetime.timezone.utc) \
        .strftime("%d/%m/%Y %H:%M:%S")