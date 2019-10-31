from api import gitlab
from utilities import types


def get_all(project_id):
    issues = []
    details = gitlab.get_issues(project_id)
    for item in details:
        issues.append(types.Issue(item['iid'], item['web_url'], item['description']))
    return issues


def sniff_secrets(issue):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({issue.web_url: issue.description})
