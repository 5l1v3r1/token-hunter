from api import gitlab


def all_snippets(projects):
    return gitlab.get_snippets(projects)
