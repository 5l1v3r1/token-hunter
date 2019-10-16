from api import gitlab
from logging import info
from osint_tools import gitlab_snippets_monitor


def all_snippets(projects):
    snippets = {}
    for project in projects:
        for key, value in project.items():
            details = gitlab.get_project_snippets(key)
            if len(details) > 0:
                info("[*] Found %s snippets for project %s", len(details), value)
            for item in details:
                snippets[item['id']] = item['web_url']
    return snippets


def get_snippet_raw(snippet_id):
    return gitlab.get_snippet_raw(snippet_id)


def sniff_secrets(snippet_ids):
    if len(snippet_ids) == 0:
        return {}
    secrets = {}
    monitor = gitlab_snippets_monitor.GitLabSnippetMonitor()
    for snippet_id in snippet_ids:
        raw_content = gitlab.get_snippet_raw(snippet_id)
        found_secrets = monitor.get_secrets(raw_content)
        if len(found_secrets) > 0:
            secrets.update(found_secrets)
    return secrets

