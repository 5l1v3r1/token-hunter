"""
Module to support logging info & output
"""

import logging as l


def configure(logging_enabled):
    # Start the logger, printing all to stdout
    l.basicConfig(format='%(message)s', level=l.INFO, stream=sys.stdout)

    # Add a logging handler for a file, if the user provides one
    if logging_enabled:
        l.getLogger().addHandler(l.FileHandler(args.logfile))
