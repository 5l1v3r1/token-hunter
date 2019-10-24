
from logging import info, warning

from api import gitlab_groups, gitlab_projects, gitlab_snippets, gitlab_members, gitlab_issues


def process_all(args):
    personal_projects = {}
    info(args)
    for group in args.group:
        group_details = gitlab_groups.get_group(group)
        if len(group_details) == 0:
            warning("[!] %s not found, skipping", group)
            continue

        group_projects = gitlab_projects.all_group_projects(group)
        members = gitlab_members.all_members(group)

        if args.members:
            for member in members:
                personal_projects.update(gitlab_projects.all_member_projects(member))

        # Print / log all the gorey details for groups and members
        log_group(group_details)
        log_projects(group_projects)
        log_members(members)

        if args.members:
            log_members_projects(personal_projects)

        # Go get the snippets content and log it if the switch is provided
        if args.snippets:
            all_snippets = gitlab_snippets.all_snippets([group_projects, personal_projects])
            all_secrets = gitlab_snippets.sniff_secrets(all_snippets)
            log_related_snippets(all_snippets, [group_projects, personal_projects])
            log_all_secrets(all_secrets, all_snippets)

        if args.issues:
            all_issues = gitlab_issues.all_issues(group)
            log_related_issues(all_issues, group)


def get_total_projects(projects):
    cnt = 0
    for project in projects:
        for item in project:
            cnt += 1
    return cnt


def log_all_secrets(all_secrets, all_snippets):
    if len(all_snippets) == 0:
        return
    info("  FOUND (%s) SECRET(S) IN (%s) TOTAL SNIPPET(S)", len(all_secrets), len(all_snippets))
    for secret in all_secrets:
        info("    Url: %s Type: %s Candidate Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_related_issues(issues, group):
    info("  FOUND (%s) TOTAL ISSUE(S) FOR GROUP (%s)", len(issues), group)
    for value in issues.values():
        info("    %s", value)


def log_related_snippets(snippets, projects):
    info("  FOUND (%s) SNIPPET(S) IN (%s) TOTAL PROJECT(S)", len(snippets), get_total_projects(projects))
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
