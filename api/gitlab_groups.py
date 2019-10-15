from api import gitlab
from logging import info


def get_group(group):
    info("[*] Fetching group details for %s", group)
    group_details = gitlab.get_group(group)
    return group_details


def all_members(group):
    return gitlab.get_members(group)


