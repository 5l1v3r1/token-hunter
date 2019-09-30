"""
GitLab specific checks for GitOSINT

These are called from the parent program, with the two core functions being:
    - process_groups
    - process_projects
"""

from logging import info, warning

from api import gitlab


def process_groups(groups):
    """
    Process a GitLab group
    """
    # There might be a lot of duplicates when process subgroups and
    # projects, so start some sets.
    personal_projects = set()

    for group in groups:
        group_details = gitlab.get_group(group)
        if not group_details:
            warning("[!] %s not found, skipping", group)
            continue

        members = gitlab.get_group_members(group)
        for member in members:
            personal_projects.update(gitlab.get_personal_projects(member))

        group_projects = gitlab.get_group_projects(group)

        # Print / log all the gorey details
        info("GROUP: %s (%s)", group_details['name'], group_details['web_url'])

        info("  GROUP PROJECTS (%s):", len(group_projects))
        for link in group_projects:
            info("    %s", link)

        info("  MEMBERS (%s):", len(members))
        for member in members:
            info("    %s", member)

        info("  MEMBERS' PERSONAL PROJECTS (%s):", len(personal_projects))
        for link in personal_projects:
            info("    %s", link)
