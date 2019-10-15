from api import gitlab
from logging import info


def get_group(group):
    info("[*] Fetching group details for %s", group)
    group_details = gitlab.get_group(group)
    return group_details


def all_members(group):
    members = []

    details = gitlab.get_members(group)
    if len(details) > 0:
        info("[*] Found %s members for group %s", len(details), group)

    for item in details:
        members.append(item['username'])

    return members



