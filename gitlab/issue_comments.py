from api import gitlab
from utilities import types


def all_comments(project_id, issue_id):
    comments = []
    detail = gitlab.get_issue_comments(project_id, issue_id)
    for item in detail:
        for note in item['notes']:
            if note['system']:  # ignore system notes:  https://docs.gitlab.com/ee/api/discussions.html
                continue
            comments.append(types.Comment('issue', "parent_url_goes_here", note['body']))
    return comments
