from api import gitlab
from logging import info, warning


def all_group_projects(group):
    return gitlab.get_group_projects(group)


def all_member_projects(member):
    personal_projects = {}
    details = gitlab.get_personal_projects(member)
    if len(details) > 0:
        info("[*] Found %s projects for member %s", len(details), member)

    for item in details:
        personal_projects[item['id']] = item['http_url_to_repo']

    return personal_projects
