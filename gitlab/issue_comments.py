from api import gitlab
from utilities import types
from api import gitlab

gitlab = gitlab.GitLab()


def get_all(project_id, issue_id, issue_web_url):
    comments = []
    detail = gitlab.get_issue_comments(project_id, issue_id)
    for item in detail:
        for note in item['notes']:
            if note['system']:  # ignore system notes:  https://docs.gitlab.com/ee/api/discussions.html
                continue
            comments.append(types.Comment('issue', issue_web_url, note['body']))
    return comments


def sniff_secrets(comment):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({comment.parent_url: comment.comment_body})
