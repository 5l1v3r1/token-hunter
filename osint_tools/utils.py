"""
Generic utilities for GitOSINT.
"""

import urllib
import datetime
import logging
import requests


def parse_targets(targets):
    """
    Parses the user-supplied targets, cleaning and ensuring they consist
    of valid URLs.

    TO DO: additional cleaning
    """
    clean_targets = set()

    for target in targets:
        target = target.lower()

        if not target.startswith('http'):
            target = 'https://' + target

        clean_targets.add(target)

    print("[*] Attempting to identify {} target url/s."
          .format(len(clean_targets)))

    return clean_targets


def identify_targets(targets):
    """
    Given a list of URLs, attempts to classify each as:
        - GitLab project
        - GitLab group
        - GitHub repo
        - GitHub team

    Returns a dictionary with the results"
    """
    classified = {}

    # Define some unique strings to identify the type of page we are on
    gl_group = 'qa-group-members-item'
    gl_project = 'js-onboarding-branches-link'
    gh_repo = 'xxxxxxxxx'
    gh_team = 'xxxxxxxxx'

    for target in targets:
        response = requests.get(target)

        if gl_group in response.text:
            classified[target] = 'gl_group'
        elif gl_project in response.text:
            classified[target] = 'gl_project'
        elif gh_repo in response.text:
            classified[target] = 'gh_repo'
        elif gh_team in response.text:
            classified[target] = 'gh_team'
        else:
            classified[target] = 'unknown'

    print("[*] Identified the following target types:")

    for item in classified:
        print("    {}: {}".format(classified[item], item))

    return classified
        

