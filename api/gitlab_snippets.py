from api import gitlab
from logging import info


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
