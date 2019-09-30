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
import datetime

from logging import info
from utilities import time, identity, validate, log, arguments
from osint_tools import gitlab_checks


def main():
    """
    Main program function
    """
    args = arguments.parse()
    log.configure(args.logfile)
    validate.environment(args)

    info("##### Git_OSINT started at UTC %s from IP %s##### ",
         time.get_current(datetime.timezone.utc), identity.get_public_ip())

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
