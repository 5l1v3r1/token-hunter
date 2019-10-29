from api import gitlab
from logging import info


def all_members(group):
    members = []

    info("[*] Fetching all members for group %s", group)
    details = gitlab.get_members(group)
    info("[*] Found %s members for group %s", len(details), group)
    for item in details:
        members.append(item['username'])

    return members
