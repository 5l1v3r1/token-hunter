"""
GitLab specific checks for GitOSINT

These are called from the parent program, with the two core functions being:
    - process_groups
    - process_projects
"""

import logging as l

from api import gitlab


def process_repos(repo):
    """
    Process a GitLab repo
    """
    l.info("Repos:  This feature is not yet implemented.")
    return


def process_projects(projects):
    """
    Process a GitLab project
    """
    l.info("Projects:  This feature is not yet implemented.")
    return


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
            l.warning("[!] %s not found, skipping", group)
            continue

        members = gitlab.get_group_members(group)
        for member in members:
            personal_projects.update(gitlab.get_personal_projects(member))

        group_projects = gitlab.get_group_projects(group)

        # Print / log all the gorey details
        l.info("GROUP: %s (%s)", group_details['name'],
               group_details['web_url'])

        l.info("  GROUP PROJECTS:")
        for link in group_projects:
            l.info("    %s", link)

        l.info("  MEMBERS:")
        for member in members:
            l.info("    %s", member)

        l.info("  MEMBERS' PERSONAL PROJECTS:")
        for link in personal_projects:
            l.info("    %s", link)
