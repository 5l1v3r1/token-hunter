import requests
import os
import re

from logging import warning, info

BASE_URL = 'https://gitlab.com/api/v4'


def get_snippets(projects):
    snippets = {}
    for project in projects:
        for key, value in project.items():
            details = get('{}/projects/{}/snippets'.format(BASE_URL, key))
            if len(details) > 0:
                info("[*] Found %s snippets for project %s", len(details), value)
            for item in details:
                snippets[item['id']] = item['web_url']
    return snippets


def get_personal_projects(member):
    """
    Returns a list of all personal projects for a member
    """
    personal_projects = {}

    details = get('{}/users/{}/projects'.format(BASE_URL, member))
    if len(details) > 0:
        info("[*] Found %s projects for member %s", len(details), member)

    for item in details:
        personal_projects[item['id']] = item['http_url_to_repo']

    return personal_projects


def get_group_projects(group):
    """
    Returns a list of all projects belonging to a group
    """
    group_projects = {}

    details = get('{}/groups/{}/projects'.format(BASE_URL, group))
    if len(details) > 0:
        info("[*] Found %s projects for group %s", len(details), group)

    for item in details:
        group_projects[item['id']] = item['http_url_to_repo']

    return group_projects


def get_group(group):
    """
    Validates access to a group via the api
    """
    info("[*] Fetching group details for %s", group)
    group_details = get('{}/groups/{}'.format(BASE_URL, group))

    if not group_details:
        return False

    return group_details


def get_group_members(group):
    """
    Returns a list of all members of a group
    """
    members = []

    details = get('{}/groups/{}/members'.format(BASE_URL, group))
    if len(details) > 0:
        info("[*] Found %s members for group %s", len(details), group)

    # We should now have a list of dictionary items, need to parse through
    # each one to extract the member info.
    for item in details:
        members.append(item['username'])

    return members


def get_current_user():
    details = get('{}/user'.format(BASE_URL))

    if not details:
        return False

    username = details['username']
    return username


def get(url):
    """
    Helper function to interact with GitLab API using python requests

    The important things here are:
        - Adding the PRIVATE-TOKEN header based on env variable
        - interacting with the pagination process via LINK headers
          (https://docs.gitlab.com/ee/api/README.html#pagination)
    """

    headers = {'PRIVATE-TOKEN': os.getenv('GITLAB_API')}
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

                regex = re.compile(r'<([^<>]*?)>; rel="next"')
                next_url = re.findall(regex, response.headers['Link'])[0]

                # Add the individual response to the collective
                response = requests.get(next_url, headers=headers)
                if response.status_code == 200:
                    all_results += response.json()
                else:
                    warning("[!] Error processing pagination URL: %s", next_url)
                pagenum += 1

            # Return the collective results
            return all_results

        # Otherwise, return just the single result
        return response.json()

    # If code not 200, no results to process
    warning("[!] API failure. Details:")
    warning("    URL: %s", url)
    warning("    Response Code: %s Reason: %s", response.status_code, response.reason)
    return False
