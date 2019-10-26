import logging
import sys


def configure(logfile):
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    if logfile:
        logging.getLogger().addHandler(logging.FileHandler(logfile))
