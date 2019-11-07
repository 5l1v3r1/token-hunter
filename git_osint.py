#!/usr/bin/env python3

from logging import info
from utilities import time, validate, log, arguments

args = None


def main():

    try:
        log.configure()
        time.log_time_stamp_start()
        validate.environment()
        validate.gitlab_api_keys()
        arguments.apply_all()
        time.log_time_stamp_end()
    except KeyboardInterrupt:
        info("[!] Keyboard Interrupt, abandon ship!")
        time.log_time_stamp_end()


if __name__ == '__main__':
    main()
