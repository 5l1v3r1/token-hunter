from api import gitlab
from utilities import types


def all_issues(group):
    issues = {}
    details = gitlab.get_issues(group)
    for item in details:
        issues.update({item['id']: item['description']})

    return issues


def sniff_secrets(issues):
    if len(issues.keys()) == 0:
        return []
    secrets = []
    monitor = types.SecretsMonitor()
    for issue_id, description in issues.items():
        found_secrets = monitor.get_secrets(description)
        for secret_type, secret in found_secrets.items():
            secrets.append(types.Secret(secret_type, secret, issue_id))
    return secrets
