from utilities import types, validate
from api import gitlab
from logging import warning

gitlab = gitlab.GitLab(types.Arguments().url)


def get_all(project_id, project_url):
    merge_requests = []
    details = gitlab.get_merge_requests(project_id)
    if validate.api_result(details):
        warning("[*] Found %s merge requests for project %s", len(details), project_url)
        for item in details:
            merge_requests.append(types.MergeRequest(item['iid'], item['web_url'], item['title']))
    return merge_requests


def sniff_secrets(mr):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({mr.web_url: mr.description})
