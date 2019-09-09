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
    Helper function to ensure API key is used if provided
    """
    api_key = os.getenv('GITLAB_API')

    if api_key:
        headers = {'PRIVATE-TOKEN': api_key}
    else:
        headers = None

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return False

def get_group(group):
    """
    Validates access to a group via the API
    """
    details = api_get('{}/groups/{}'.format(API, group))

    if not details:
        return False
    else:
        l.info("GROUP: %s (%s)", details['name'], details['web_url'])
        return True

def get_group_members(group):
    """
    Returns a list of all members of a group
    """
    members = []
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
    details = api_get('{}/users/{}/projects'.format(API, member))
    project_urls = []

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
        l.info("  MEMBERS:")
        for member in members:
            l.info("    %s", member)
        #group_projects = get_group_projects(group)

        for member in members:
            personal_projects.update(get_personal_projects(member))

        l.info("  PERSONAL PROJECTS:")
        for link in personal_projects:
            l.info("    %s", link)

