"""
GitLab specific checks for GitOSINT
"""

import re
import os
import logging as l
import requests


API = 'https://gitlab.com/api/v4'
API_KEY = None

def api_get(url):
    """
    Helper function to interact with GitLab API using python requests

    The important things here are:
        - Adding the PRIVATE-TOKEN header if using an API key
        - interacting with the pagination process via LINK headers
          (https://docs.gitlab.com/ee/api/README.html#pagination)
    """
    api_key = os.getenv('GITLAB_API')

    if api_key:
        headers = {'PRIVATE-TOKEN': api_key}
    else:
        headers = None

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # The "Link" header is returned when there is more than one page of
        # results. GitLab asks that we use this link instead of crafting
        # our own.
        if 'Link' in response.headers.keys():
            # initialize a new variable to begin compounding multi-page
            # results
            all_results = response.json()
            # Now, loop through until there is no 'next' link provided
            pagenum = 1
            while 'rel="next"' in response.headers['Link']:
                # Using print instead of logging, we don't want the per-page
                # status update in the log file
                print("[*] Processing page {}\r".format(pagenum), end='')

                regex = re.compile(r'<([^<>]*?)>; rel="next"')
                next_url = re.findall(regex, response.headers['Link'])[0]

                # Add the individual response to the collective
                response = requests.get(next_url, headers=headers)
                all_results += response.json()

                pagenum += 1

            # We need a line break if we've counted pages
            if pagenum > 1:
                print("")

            # Return the collective retuls
            return all_results

        else:
            return response.json()
    else:
        return False

def get_group(group):
    """
    Validates access to a group via the API
    """
    l.info("[*] Fetching group details for %s", group)
    details = api_get('{}/groups/{}'.format(API, group))

    if not details:
        return False
    else:
        return True

def get_group_members(group):
    """
    Returns a list of all members of a group
    """
    members = []

    l.info("[*] Fetching group members for %s", group)
    details = api_get('{}/groups/{}/members'.format(API, group))

    # We should now have a list of dictionary items, need to parse through
    # each one to extract the member info.
    for item in details:
        members.append(item['username'])

    return members

def get_personal_projects(member):
    """
    Returns a list of all personal projects for a member
    """
    project_urls = []

    l.info("[*] Fetching personal projects for %s", member)
    details = api_get('{}/users/{}/projects'.format(API, member))

    if not details:
        pass

    for item in details:
        project_urls.append(item['web_url'])

    return project_urls

def process_project(target):
    """
    Process a GitLab project
    """
    return

def process_groups(groups):
    """
    Process a GitLab group
    """
    # There might be a lot of duplicates when process subgroups and
    # projects, so start some sets.
    total_members = set()
    group_projects = set()
    personal_projects = set()

    for group in groups:
        if not get_group(group):
            l.warning("[!] %s not found, skipping", group)
            continue

        members = get_group_members(group)
        for member in members:
            personal_projects.update(get_personal_projects(member))
        #group_projects = get_group_projects(group)

        # Print / log all the gorey details
        l.info("GROUP: %s (%s)", details['name'], details['web_url'])

        l.info("  MEMBERS:")
        for member in members:
            l.info("    %s", member)

        l.info("  PERSONAL PROJECTS:")
        for link in personal_projects:
            l.info("    %s", link)

