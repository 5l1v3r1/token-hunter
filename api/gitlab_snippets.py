from api import gitlab
from logging import info
from osint_tools import gitlab_snippets_monitor
from utilities import snippet


def all_snippets(projects):
    snippets = {}
    for project in projects:
        for key, value in project.items():
            details = gitlab.get_project_snippets(key)
            if len(details) > 0:
                info("[*] Found %s snippets for project %s", len(details), value)
            for item in details:
                snippets.update({item['id']: item['web_url']})
    return snippets


def get_snippet_raw(snippet_id):
    return gitlab.get_snippet_raw(snippet_id)


def sniff_secrets(snippets):
    if len(snippets.keys()) == 0:
        return []
    secrets = []
    monitor = gitlab_snippets_monitor.GitLabSnippetMonitor()
    for snippet_id, snippet_url in snippets.items():
        raw_content = gitlab.get_snippet_raw(snippet_id)
        found_secrets = monitor.get_secrets(raw_content)
        for secret_type, secret in found_secrets.items():
            secrets.append(snippet.SnippetSecret(secret_type, secret, snippet_url))
    return secrets
