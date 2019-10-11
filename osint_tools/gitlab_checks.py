"""
GitLab specific checks for GitOSINT

These are called from the parent program, with the two core functions being:
    - process_groups
    - process_projects
"""

from logging import info, warning

from api import gitlab


def process_groups(groups, snippets):
    """
    Process a GitLab group
    """
    # There might be a lot of duplicates when process subgroups and
    # projects, so start some sets.
    personal_projects = {}

    for group in groups:
        group_details = gitlab.get_group(group)
        if not group_details:
            warning("[!] %s not found, skipping", group)
            continue

        group_projects = gitlab.get_group_projects(group)
        members = gitlab.get_group_members(group)

        for member in members:
            personal_projects.update(gitlab.get_personal_projects(member))

        if snippets:
            all_snippets = gitlab.get_snippets([group_projects, personal_projects])

        # Print / log all the gorey details
        log_group(group_details)
        log_projects(group_projects)
        log_members(members)
        log_members_projects(personal_projects)
        if snippets:
            log_related_snippets(all_snippets, [group_projects, personal_projects])


def get_total_projects(projects):
    cnt = 0
    for project in projects:
        for item in project:
            cnt += 1
    return cnt


def log_related_snippets(snippets, projects):
    info("  FOUND (%s) SNIPPETS IN (%s) TOTAL PROJECTS", len(snippets), get_total_projects(projects))
    for value in snippets.values():
        info("    %s", value)


def log_group(group_details):
    info("GROUP: %s (%s)", group_details['name'], group_details['web_url'])


def log_projects(group_projects):
    info("  GROUP PROJECTS (%s):", len(group_projects))
    for value in group_projects.values():
        info("    %s", value)


def log_members(members):
    info("  MEMBERS (%s):", len(members))
    for member in members:
        info("    %s", member)


def log_members_projects(personal_projects):
    info("  MEMBERS' PERSONAL PROJECTS (%s):", len(personal_projects))
    for value in personal_projects.values():
        info("    %s", value)
