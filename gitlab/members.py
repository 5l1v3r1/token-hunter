from api import gitlab
from logging import info
from api import gitlab

gitlab = gitlab.GitLab()


def get_all(group):
    members = []

    info("[*] Fetching all members for group %s", group)
    details = gitlab.get_members(group)
    info("[*] Found %s members for group %s", len(details), group)
    for item in details:
        members.append(item['username'])

    return members
