"""
GitLab specific checks for GitOSINT
"""

import re
import requests

def get_project_members(target):
    """
    Returns a list of all members in a project
    """
    members_page = target + '/-/group_members'
    print("[*] Scraping {} for members".format(members_page))

    response = requests.get(members_page)

    regex = re.compile(r'js-last-button.*?page=(.*?)"')
    members = re.findall(regex, response.text)

    print(members)
    return members

def get_personal_projects(members):
    """
    Returns a list of all personal projects for a list of members
    """
    return

def process_project(target):
    """
    Process a GitLab project
    """
    return

def process_group(target):
    """
    Process a GitLab group
    """
    members = get_project_members(target)
    personal_projects = get_personal_projects(members)

