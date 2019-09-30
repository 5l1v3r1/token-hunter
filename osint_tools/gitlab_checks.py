"""
GitLab specific checks for GitOSINT

These are called from the parent program, with the two core functions being:
    - process_groups
    - process_projects
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
        - Adding the PRIVATE-TOKEN header based on env variable
        - interacting with the pagination process via LINK headers
          (https://docs.gitlab.com/ee/api/README.html#pagination)
    """
    api_key = os.getenv('GITLAB_API')

    if api_key:
        headers = {'PRIVATE-TOKEN': api_key}
    else:
        # Leaving this for possible future use, but program will actually
        # sys.exit prior to this without an API key set.
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
            pagenum = 2
            while 'Link' in response.headers.keys() and 'rel="next"' in response.headers['Link']:
                # Using print instead of logging, we don't want the per-page
                # status update in the log file
                print("[*] Processing page {}\r".format(pagenum), end='')

                regex = re.compile(r'<([^<>]*?)>; rel="next"')
                next_url = re.findall(regex, response.headers['Link'])[0]

                # Add the individual response to the collective
                response = requests.get(next_url, headers=headers)
                if response.status_code == 200:
                    all_results += response.json()
                else:
                    l.warning("[!] Error processing pagination URL: %s", next_url)
                pagenum += 1

            # We need a line break if we've counted pages
            if pagenum > 1:
                print("")

            # Return the collective retuls
            return all_results

        # Otherwise, return just the single result
        return response.json()

    # If code not 200, no results to process
    l.warning("[!] API failure. Details:")
    l.warning("    URL: %s", url)
    l.warning("    Response Code: %s Reason: %s", response.status_code, response.reason)
    return False

def get_current_user():
    """
    Gets the current username, based on API key.
    """
    details = api_get('{}/user'.format(API))

    if not details:
        return False

    username = details['username']
    return username

def get_group(group):
    """
    Validates access to a group via the API
    """
    l.info("[*] Fetching group details for %s", group)
    group_details = api_get('{}/groups/{}'.format(API, group))

    if not group_details:
        return False

    return group_details

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

def get_group_projects(group):
    """
    Returns a list of all projects belonging to a group
    """
    project_urls = []

    l.info("[*] Fetching group projects for %s", group)
    details = api_get('{}/groups/{}/projects'.format(API, group))

    if not details:
        pass

    for item in details:
        project_urls.append(item['http_url_to_repo'])

    return project_urls

def get_personal_projects(member):
    """
    Returns a list of all personal projects for a member
    """
    project_urls = []

    l.info("[*] Fetching personal projects for %s", member)
    details = api_get('{}/users/{}/projects'.format(API, member))

    if not details:
        return []

    for item in details:
        project_urls.append(item['http_url_to_repo'])

    return project_urls

def process_repos(repo):
    """
    Process a GitLab repo
    """
    l.info("Repos:  This feature is not yet implemented.")
    return

def process_projects(projects):
    """
    Process a GitLab project
    """
    l.info("Projects:  This feature is not yet implemented.")
    return

def process_groups(groups):
    """
    Process a GitLab group
    """
    # There might be a lot of duplicates when process subgroups and
    # projects, so start some sets.
    personal_projects = set()

    for group in groups:
        group_details = get_group(group)
        if not group_details:
            l.warning("[!] %s not found, skipping", group)
            continue

        members = get_group_members(group)
        for member in members:
            personal_projects.update(get_personal_projects(member))

        group_projects = get_group_projects(group)

        # Print / log all the gorey details
        l.info("GROUP: %s (%s)", group_details['name'],
               group_details['web_url'])

        l.info("  GROUP PROJECTS:")
        for link in group_projects:
            l.info("    %s", link)

        l.info("  MEMBERS:")
        for member in members:
            l.info("    %s", member)

        l.info("  MEMBERS' PERSONAL PROJECTS:")
        for link in personal_projects:
            l.info("    %s", link)
