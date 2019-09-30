#!/usr/bin/env python3

"""
GitOSINT!

Learn more about your friends and colleagues. Provide this tool with
the URL of git project, group, repo, or team. GitOSINT will crawl the site,
looking for the following:
    - personal projects of all members, contributors
    - social media profiles of everyone involved
    - (more to come)
"""

from logging import warning, info

import datetime

import os

from utilities import time, identity, validate, log, arguments

from osint_tools import gitlab_checks


def check_env(args):
    """
    Check for environment variables
    """
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


def main():
    """
    Main program function
    """
    args = arguments.parse()
    log.configure(args.logfile)

    info("##### Git_OSINT started at UTC %s from IP %s##### ",
         time.get_current(datetime.timezone.utc), identity.get_public_ip())

    # Verify we have environment variables set for expected APIs
    check_env(args)

    # Run an initial API call to validate API keys
    if args.group or args.project or args.snippets:
        validate.gitlab_api_keys(args)

    # Run the appropriate checks for each type
    try:
        apply_args(args)
    except KeyboardInterrupt:
        info("[!] Keyboard Interrupt, abandon ship!")

    info("##### Git_OSINT finished at UTC %s ##### ", time.get_current_utc())


def apply_args(args):
    switcher = {
        args.group: gitlab_checks.process_groups(args.group),
        args.project: gitlab_checks.process_projects(args.project),
        args.team: gitlab_checks.process_projects(args.team),
        args.repo: gitlab_checks.process_repos(args.repo)
    }


if __name__ == '__main__':
    main()
