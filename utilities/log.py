import logging
import sys
from utilities import arguments


def configure():
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)
    logfile = arguments.parsed_args.logfile
    if logfile:
        logging.getLogger().addHandler(logging.FileHandler(logfile))
