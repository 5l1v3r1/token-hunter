"""
Module to support logging info & output
"""

import logging
import sys


def configure(logfile):
    # Start the logger, printing all to stdout
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    # Add a logging handler for a file, if the user provides one
    if logfile:
        logging.getLogger().addHandler(logging.FileHandler(logfile))
