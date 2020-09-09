import logging
import sys
import coloredlogs

from utilities import types

args = types.Arguments()


def configure():
    coloredlogs.install(level='INFO', fmt="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)
    logfile = args.logfile
    if logfile:
        logging.getLogger().addHandler(logging.FileHandler(logfile))
