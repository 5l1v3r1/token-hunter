from api import gitlab
from utilities import types


def all_issues(group):
    issues = {}
    details = gitlab.get_issues(group)
    for item in details:
        issues.update({item['web_url']: item['description']})
    return issues


def sniff_secrets(issues):
    if len(issues.keys()) == 0:
        return []
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets(issues)
