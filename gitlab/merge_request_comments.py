from api import gitlab
from utilities import validate, types
from logging import info

gitlab = gitlab.GitLab(types.Arguments().url)


def get_all(project_id, mr_id, mr_web_url):
    comments = []
    detail = gitlab.get_merge_request_comments(project_id, mr_id)
    if validate.api_result(detail):
        legit_comments = 0
        for item in detail:
            for note in item['notes']:
                if note['system']:  # ignore system notes:  https://docs.gitlab.com/ee/api/discussions.html
                    continue
                comments.append(types.Comment('merge_request', mr_web_url, note['body']))
                legit_comments += 1
        if legit_comments > 0:
            info("[*] Found %s comments for merge request %s", legit_comments, mr_web_url)
    return comments


def sniff_secrets(comment):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({comment.parent_url: comment.comment_body})
