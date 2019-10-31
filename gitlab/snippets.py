from api import gitlab
from utilities import types


def get_all(projects):
    snippets = {}
    for project in projects:
        for key, value in project.items():
            details = gitlab.get_project_snippets(key)
            for item in details:
                snippets.update({item['id']: item['web_url']})
    return snippets


def sniff_secrets(snippets):
    if len(snippets.keys()) == 0:
        return []
    secrets = []
    raw_data = {}
    for snippet_id, snippet_url in snippets.items():
        raw_content = gitlab.get_snippet_raw(snippet_id)
        raw_data.update({snippet_url: raw_content})
    if len(raw_data) > 0:
        monitor = types.SecretsMonitor()
        found_secrets = monitor.sniff_secrets(raw_data)
        if len(found_secrets) > 0:
            secrets.append(found_secrets)
    return secrets
