from utilities import types, validate
from api import gitlab

gitlab = gitlab.GitLab()


def get_all(project_id):
    issues = []
    details = gitlab.get_issues(project_id)
    if validate.api_result(details):
        for item in details:
            issues.append(types.Issue(item['iid'], item['web_url'], item['description']))
    return issues


def sniff_secrets(issue):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({issue.web_url: issue.description})
