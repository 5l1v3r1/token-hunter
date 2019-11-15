from logging import info
from api import gitlab
from utilities import validate

gitlab = gitlab.GitLab()


def get_all(group):
    members = []

    info("[*] Fetching all members for group %s", group)
    details = gitlab.get_members(group)
    if validate.api_result(details):
        info("[*] Found %s members for group %s", len(details), group)
        for item in details:
            members.append(item['username'])

    return members
