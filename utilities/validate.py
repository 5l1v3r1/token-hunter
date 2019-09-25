"""
Module to support validation of configuration and supplied params
"""
import sys
import logging as l
from osint_tools import gitlab_checks

def gitlab_api_keys(args):
    """
    Tests GitLab API authentication prior to continuing
    """
    username = gitlab_checks.get_current_user()
    if not username:
        l.warning("[!] Cannot validate GitLab API key.")
        sys.exit()

    l.info("[*] Using GitLab API key assigned to username: %s", username)