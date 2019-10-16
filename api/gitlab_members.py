from api import gitlab
from logging import info


def all_members(group):
    members = []

    details = gitlab.get_members(group)
    if len(details) > 0:
        info("[*] Found %s members for group %s", len(details), group)

    for item in details:
        members.append(item['username'])

    return members
