from logging import info
from api import gitlab

gitlab = gitlab.GitLab()


def get(group):
    info("[*] Fetching group details for %s", group)
    return gitlab.get_group(group)





