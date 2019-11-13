"""
Module to support validation of configuration and supplied params
"""
import sys
import os

from logging import warning, info
from api import gitlab
from utilities import constants

gitlab = gitlab.GitLab()


def gitlab_api_keys():
    username = gitlab.get_current_user()
    if not username:
        warning("[!] Cannot validate GitLab API key.")
        sys.exit()

    info("[*] Using GitLab API Token assigned to username: %s", username)


def environment():
    if not os.getenv(constants.Environment.gitlab_api_token()):
        warning(f"[!] {constants.Environment.gitlab_api_token()} environment variable is not set.")
        sys.exit()
    else:
        info(f"[*] {constants.Environment.gitlab_api_token()} is configured and will be used.")
