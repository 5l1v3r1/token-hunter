from api import gitlab
from utilities import types


def get_all(project_id, issue_id):
    comments = []
    detail = gitlab.get_issue_comments(project_id, issue_id)
    for item in detail:
        for note in item['notes']:
            if note['system']:  # ignore system notes:  https://docs.gitlab.com/ee/api/discussions.html
                continue
            comments.append(types.Comment('issue', "parent_url_goes_here", note['body']))
    return comments


def sniff_secrets(comment):
    if not comment == 0:
        return []
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({comment.parent_url, comment.comment_body})