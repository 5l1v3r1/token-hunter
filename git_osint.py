#!/usr/bin/env python3
import datetime

from logging import info
from utilities import time, identity, validate, log, arguments


def main():
    """
    Main program function
    """
    args = arguments.parse()
    log.configure(args.logfile)
    validate.environment()

    if args.timestamp:
        info("##### Git_OSINT started at UTC %s from IP %s##### ",
             time.get_current(datetime.timezone.utc), identity.get_public_ip())

    validate.gitlab_api_keys(args)

    # Run the appropriate checks for each type
    try:
        arguments.apply_all(args)
    except KeyboardInterrupt:
        info("[!] Keyboard Interrupt, abandon ship!")

    if args.timestamp:
        info("##### Git_OSINT finished at UTC %s ##### ", time.get_current(datetime.timezone.utc))


if __name__ == '__main__':
    main()
