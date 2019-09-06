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

import sys
import os
import argparse
import requests
from osint_tools import utils
from osint_tools import gitlab_checks
from osint_tools import github_checks

def parse_arguments():
    """
    Parse user-supplied arguments
    """
    desc = "Collect OSINT from GitLab and GitHub"
    parser = argparse.ArgumentParser(description=desc)

    target_group = parser.add_mutually_exclusive_group(required=True)

    target_group.add_argument('-u', '--url', type=str, action='append',
                              help='URL of a git project, group, repo, or team')
    target_group.add_argument('-i', '--infile', type=str, action='store',
                              help='Input file with one URL per line')

    parser.add_argument('-l', '--logfile', type=str, action='store',
                        help='Will APPEND found items to specified file.')

    args = parser.parse_args()

    # Process the input file if provided. Return a list of targets.
    if args.infile:
        if not os.access(args.infile, os.R_OK):
            print("[!] Cannot access input file, exiting")
            sys.exit()
        else:
            with open(args.infile) as infile:
                args.targets = [target.strip() for target in infile]
    else:
        args.targets = args.url

    # Ensure log file is writeable
    if args.logfile:
        if os.path.isdir(args.logfile):
            print("[!] Can't specify a directory as the logfile, exiting.")
            sys.exit()
        if os.path.isfile(args.logfile):
            target = args.logfile
        else:
            target = os.path.dirname(args.logfile)
            if target == '':
                target = '.'

        if not os.access(target, os.W_OK):
            print("[!] Cannot write to log file, exiting")
            sys.exit()

        # Set the global in the utils file, where logging needs to happen
        utils.init_log(args.logfile)

    return args


def main():
    """
    Main program function
    """
    args = parse_arguments()

    # Clean all input into usable URLs
    targets = utils.parse_targets(args.targets)

    # Identify the target type for each clean URL
    classified = utils.identify_targets(targets)

    # Run the appropriate checks for each type
    for target in classified:
        if classified[target] == 'gl_group':
            gitlab_checks.process_group(target)
        elif classified[target] == 'gl_project':
            gitlab_checks.process_project(target)
        elif classified[target] == 'gh_repo':
            github_checks.process_repo(target)
        elif classified[target] == 'gh_team':
            github_checks.process_team(target)

if __name__ == '__main__':
    main()
