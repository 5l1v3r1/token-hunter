"""
Module to support validation of configuration and supplied params
"""
import sys
import os

from logging import warning, info
from api import gitlab


def gitlab_api_keys(args):
    username = gitlab.get_current_user()
    if not username:
        warning("[!] Cannot validate GitLab API key.")
        sys.exit()

    info("[*] Using GitLab API key assigned to username: %s", username)


def environment():
    if not os.getenv('GITLAB_API'):
        warning("[!] GITLAB_API environment variable is not set.")
        sys.exit()
    else:
        info("[*] GITLAB_API is configured and will be used.")
