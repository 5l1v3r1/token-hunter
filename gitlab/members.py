from api import gitlab
from logging import info


def all_members(group):
    members = []

    info("[*] Fetching all members for group %s")
    details = gitlab.get_members(group)
    if len(details) > 0:
        info("[*] Found %s members for group %s", len(details), group)
    else:
        info("[*] No members found for group %s", group)

    for item in details:
        members.append(item['username'])

    return members
