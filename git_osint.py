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

import logging as l
import datetime
import sys
import os
import argparse
import requests

from utilities import time, identity, validate

from osint_tools import gitlab_checks
from osint_tools import github_checks

def parse_arguments():
    """
    Parse user-supplied arguments
    """
    desc = "Collect OSINT from GitLab and GitHub"
    parser = argparse.ArgumentParser(description=desc)

    # Any combination, including multiple of each, of projects,
    # groups, repos, and teams.
    parser.add_argument('-g', '--group', type=str, action='append',
                        help='Name of a GitLab group')
    parser.add_argument('-p', '--project', type=str, action='append',
                        help='Name of a GitLab project')
    parser.add_argument('-t', '--team', type=str, action='append',
                        help='Name of a GitHub team')
    parser.add_argument('-r', '--repo', type=str, action='append',
                        help='Name of a GitHub repo')
    parser.add_argument('-s', '--snippets', type=str, action='append',
        help="Enable search for snippets in gitlab for secrets")

    parser.add_argument('-l', '--logfile', type=str, action='store',
                        help='Will APPEND found items to specified file.')
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Start the logger, printing all to stdout
    l.basicConfig(format='%(message)s', level=l.INFO, stream=sys.stdout)

    # Add a logging handler for a file, if the user provides one
    if args.logfile:
        l.getLogger().addHandler(l.FileHandler(args.logfile))

    return args

def check_env(args):
    """
    Check for environment variables
    """
    if args.group or args.project:
        if not os.getenv('GITLAB_API'):
            l.warning("[!] GITLAB_API environment variable is not set.")
            sys.exit()
        else:
            l.info("[*] GITLAB_API is configured and will be used.")
    if args.team or args.repo:
        if not os.getenv('GITHUB_API'):
            l.warning("[!] GITHUB_API environment variable is not set.")
            sys.exit()
        else:
            l.info("[*] GITHUB_API is configured and will be used.")

def main():
    """
    Main program function
    """
    args = parse_arguments()

    l.info("##### Git_OSINT started at UTC %s from IP %s##### ",
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
        l.info("[!] Keyboard Interrupt, abandon ship!")

    l.info("##### Git_OSINT finished at UTC %s ##### ", time.get_current_utc())

def apply_args(args):
    switcher = {
        args.group: gitlab_checks.process_groups(args.group),
        args.project: gitlab_checks.process_projects(args.project),
        args.team: gitlab_checks.process_projects(args.team),
        args.repo: gitlab_checks.process_repos(args.repo)
    }

if __name__ == '__main__':
    main()
