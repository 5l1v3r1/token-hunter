from api import gitlab
from logging import info
from api import gitlab

gitlab = gitlab.GitLab()


def get(group):
    info("[*] Fetching group details for %s", group)
    group_details = gitlab.get_group(group)
    return group_details






