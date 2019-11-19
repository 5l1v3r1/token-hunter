from logging import info, warning
from utilities import types
from gitlab import projects, snippets, groups, issues, members, issue_comments


def analyze():

    personal_projects = {}
    args = types.Arguments()

    for group in args.group:
        group_details = groups.get(group)
        if group_details is False:
            warning("[!] %s not found, skipping", group)
            continue

        group_projects = projects.all_group_projects(group)
        all_members = members.get_all(group)

        if args.members:
            for member in all_members.keys():
                personal_projects.update(projects.all_member_projects(member))

        all_projects = {**group_projects, **personal_projects}

        log_group(group_details)
        log_group_projects(group_projects)
        log_members(all_members)

        if args.members:
            log_members_projects(personal_projects)

        if args.snippets:
            info("[*] Fetching snippets for %s projects", len(all_projects))
            all_secrets = []
            all_snippets = snippets.get_all([group_projects, personal_projects])
            secrets_list = snippets.sniff_secrets(all_snippets)
            for secret in secrets_list:
                all_secrets.append(secret)
            log_related_snippets(all_snippets, all_projects)
            log_snippet_secrets(all_secrets, all_snippets)

        if args.issues:
            info("[*] Fetching issues & comments for all projects")
            all_issues = []
            all_comments = []
            all_secrets = []
            # loop each project (personal or group)
            for project_id, project_url in all_projects.items():
                # loop each issue in the project and search for secrets in the description
                project_issues = issues.get_all(project_id, project_url)
                for issue in project_issues:
                    all_issues.append(issue)
                    secrets = issues.sniff_secrets(issue)
                    for secret in secrets:
                        all_secrets.append(secret)
                    # loop the comments for each issue searching for secrets in the body
                    comments = issue_comments.get_all(project_id, issue.ident, issue.web_url)
                    for comment in comments:
                        all_comments.append(comment)
                        secrets = issue_comments.sniff_secrets(comment)
                        for secret in secrets:
                            all_secrets.append(secret)

            log_related_issues_comments(all_issues, all_comments, all_projects)
            log_issue_comment_secrets(all_secrets, all_issues, all_comments)


def log_issue_comment_secrets(secrets, all_issues, all_comments):
    info("   FOUND %s SECRETS IN %s TOTAL ISSUES & COMMENTS", len(secrets), len(all_issues) + len(all_comments))
    for secret in secrets:
        info("     Url: %s Type: %s Candidate Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_snippet_secrets(all_secrets, all_snippets):
    info("   FOUND %s SECRETS IN %s TOTAL SNIPPETS", len(all_secrets), len(all_snippets))
    for secret in all_secrets:
        info("       Url: %s Type: %s Candidate Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_related_issues_comments(all_issues, all_comments, all_projects):
    info("  FOUND %s ISSUES AND %s COMMENTS ACROSS %s PROJECTS", len(all_issues), len(all_comments), len(all_projects))


def log_related_snippets(all_snippets, all_projects):
    info("  FOUND %s SNIPPETS ACROSS %s TOTAL PROJECTS", len(all_snippets), len(all_projects))


def log_group(group_details):
    info("GROUP: %s (%s)", group_details['name'], group_details['web_url'])


def log_group_projects(group_projects):
    info("  GROUP PROJECTS (%s):", len(group_projects))
    for value in group_projects.values():
        info("    %s", value)


def log_members(all_members):
    info("  MEMBERS (%s):", len(all_members))
    for member, web_url in all_members.items():
        info("    %s (%s)", member, web_url)


def log_members_projects(personal_projects):
    info("  MEMBERS' PERSONAL PROJECTS (%s):", len(personal_projects))
    for value in personal_projects.values():
        info("    %s", value)
