#!/usr/bin/env python3

from logging import info
from utilities import time, validate, log, arguments


def main():

    try:
        args = arguments.parse()
        log.configure(args.logfile)
        validate.environment()
        validate.gitlab_api_keys(args)
        time.log_time_stamp_start(args.timestamp)
        arguments.apply_all(args)
        time.log_time_stamp_end(args.timestamp)
    except KeyboardInterrupt:
        info("[!] Keyboard Interrupt, abandon ship!")
        time.log_time_stamp_end(args.timestamp)


if __name__ == '__main__':
    main()
