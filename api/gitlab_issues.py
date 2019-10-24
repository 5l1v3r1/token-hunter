from api import gitlab
from logging import info


def all_issues(group):
    issues = {}

    details = gitlab.get_issues(group)
    if len(details) > 0:
        info("[*] Found %s issues for group %s", len(details), group)

    for item in details:
        issues.update({item['id']: item['web_url']})

    return issues
