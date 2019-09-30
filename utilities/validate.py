"""
Module to support validation of configuration and supplied params
"""
import sys
import os

from logging import warning, info
from osint_tools import gitlab_checks


def gitlab_api_keys(args):
    """
    Tests GitLab API authentication prior to continuing
    """
    if not args.group or not args.project or not args.snippets:
        return

    username = gitlab_checks.get_current_user()
    if not username:
        warning("[!] Cannot validate GitLab API key.")
        sys.exit()

    info("[*] Using GitLab API key assigned to username: %s", username)


def environment(args):
    if args.group or args.project:
        if not os.getenv('GITLAB_API'):
            warning("[!] GITLAB_API environment variable is not set.")
            sys.exit()
        else:
            info("[*] GITLAB_API is configured and will be used.")
    if args.team or args.repo:
        if not os.getenv('GITHUB_API'):
            warning("[!] GITHUB_API environment variable is not set.")
            sys.exit()
        else:
            info("[*] GITHUB_API is configured and will be used.")
