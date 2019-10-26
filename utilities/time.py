import datetime

from utilities import identity
from logging import info


def get_current(timezone):
    return datetime.datetime.now(timezone) \
        .strftime("%d/%m/%Y %H:%M:%S")


def log_time_stamp_start(arg):
    if arg:
        info("##### Git_OSINT started at UTC %s from IP %s##### ",
             get_current(datetime.timezone.utc), identity.get_public_ip())


def log_time_stamp_end(arg):
    if arg:
        info("##### Git_OSINT finished at UTC %s ##### ", get_current(datetime.timezone.utc))
