from logging import info, warning
from utilities import types
from gitlab import \
    projects, snippets, groups, \
    issues, members, issue_comments, \
    merge_requests, merge_request_comments, \
    job_logs


def analyze():
    all_issues = []
    all_issue_comments = []
    all_merge_requests = []
    all_mr_comments = []
    all_job_logs = []
    personal_projects = {}
    all_snippets = {}
    args = types.Arguments()

    for group in args.group:
        group_details = groups.get(group)
        if group_details is False:
            warning("[!] %s not found, skipping", group)
            continue

        group_projects = projects.all_group_projects(group)
        all_members = members.get_all(group)

        if args.members:
            for member in all_members:
                personal_projects.update(projects.all_member_projects(member))

        all_projects = {**group_projects, **personal_projects}

        log_group(group_details)
        log_group_projects(group_projects)
        log_members(all_members)

        if args.members:
            log_members_projects(personal_projects)

        if args.snippets:
            info("[*] Fetching snippets for %s projects", len(all_projects))
            all_snippets = snippets.get_all([group_projects, personal_projects])

        if args.issues:
            info("[*] Fetching issues & comments for %s projects", len(all_projects))
            # loop each project (personal or group)
            for project_id, project_url in all_projects.items():
                # loop each issue in the project and search for secrets in the description
                project_issues = issues.get_all(project_id, project_url)
                for issue in project_issues:
                    all_issues.append(issue)

                    # loop the comments for each issue searching for secrets in the body
                    comments = issue_comments.get_all(project_id, issue.ident, issue.web_url)
                    for comment in comments:
                        all_issue_comments.append(comment)

        if args.mergerequests:
            info("[*] Fetching merge requests discussions for %s projects", len(all_projects))
            for project_id, project_url in all_projects.items():
                project_merge_requests = merge_requests.get_all(project_id, project_url)
                for mr in project_merge_requests:
                    all_merge_requests.append(mr)

                    # loop the comments for each merge request searching for secrets in the body
                    comments = merge_request_comments.get_all(project_id, mr.ident, mr.web_url)
                    for comment in comments:
                        all_mr_comments.append(comment)

        if args.jobs:
            info("[*] Fetching CI job logs for %s projects", len(all_projects))
            for project_id, project_url in all_projects.items():
                project_job_logs = job_logs.get_all(project_id, project_url)
                if len(project_job_logs) > 0:
                    for log in project_job_logs:
                        all_job_logs.append(log)

        get_snippet_secrets(all_snippets, all_projects, args)
        get_issues_comments_secrets(all_issues, all_issue_comments, all_projects, args)
        get_merge_reqs_comments_secrets(all_merge_requests, all_mr_comments, all_projects, args)
        get_job_log_secrets(all_job_logs, all_projects, args)


def get_job_log_secrets(all_job_logs, all_projects, args):
    if args.jobs:
        info("[*] Sniffing for secrets in job logs")
        all_secrets = []
        for log in all_job_logs:
            secrets = job_logs.sniff_secrets(log)
            for secret in secrets:
                all_secrets.append(secret)
        log_related_jobs(all_job_logs, all_projects)
        log_job_secrets(all_secrets, all_job_logs)


def get_merge_reqs_comments_secrets(all_merge_requests, all_mr_comments, all_projects, args):
    if args.mergerequests:
        info("[*] Sniffing for secrets in merge requests and merge request comments")
        all_secrets = []
        for mr in all_merge_requests:
            secrets = merge_requests.sniff_secrets(mr)
            for secret in secrets:
                all_secrets.append(secret)
        for comment in all_mr_comments:
            secrets = merge_request_comments.sniff_secrets(comment)
            for secret in secrets:
                all_secrets.append(secret)
        log_related_mrs_comments(all_merge_requests, all_mr_comments, all_projects)
        log_mrs_comments_secrets(all_secrets, all_merge_requests, all_mr_comments)


def get_issues_comments_secrets(all_issues, all_issue_comments, all_projects, args):
    if args.issues:
        info("[*] Sniffing for secrets in issues and issue comments")
        all_secrets = []
        for issue in all_issues:
            secrets = issues.sniff_secrets(issue)
            for secret in secrets:
                all_secrets.append(secret)
        for comment in all_issue_comments:
            secrets = issue_comments.sniff_secrets(comment)
            for secret in secrets:
                all_secrets.append(secret)
        log_related_issues_comments(all_issues, all_issue_comments, all_projects)
        log_issue_comment_secrets(all_secrets, all_issues, all_issue_comments)


def get_snippet_secrets(all_snippets, all_projects, args):
    if args.snippets:
        info("[*] Sniffing for secrets in found snippets")
        all_secrets = []
        secrets_list = snippets.sniff_secrets(all_snippets)
        for s in secrets_list:
            all_secrets.append(s)
        log_related_snippets(all_snippets, all_projects)
        log_snippet_secrets(all_secrets, all_snippets)


def log_related_mrs_comments(all_merge_requests, all_mr_comments, all_projects):
    info("  FOUND %s MERGE REQUESTS AND %s COMMENTS ACROSS %s PROJECTS", len(all_merge_requests), len(all_mr_comments), len(all_projects))


def log_mrs_comments_secrets(secrets, all_issues, all_comments):
    info("   FOUND %s SECRETS IN %s TOTAL MERGE REQUESTS & COMMENTS", len(secrets), len(all_issues) + len(all_comments))
    for secret in sorted(secrets, key=lambda i: (len(i.url), i.url)):
        info("      Url: %s, Type: %s, Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_issue_comment_secrets(secrets, all_issues, all_comments):
    info("   FOUND %s SECRETS IN %s TOTAL ISSUES & COMMENTS", len(secrets), len(all_issues) + len(all_comments))
    for secret in sorted(secrets, key=lambda i: (len(i.url), i.url)):
        info("      Url: %s, Type: %s, Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_snippet_secrets(all_secrets, all_snippets):
    info("   FOUND %s SECRETS IN %s TOTAL SNIPPETS", len(all_secrets), len(all_snippets))
    for secret in sorted(all_secrets, key=lambda i: (len(i.url), i.url)):
        info("      Url: %s, Type: %s, Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_job_secrets(all_secrets, all_jobs):
    info("   FOUND %s SECRETS IN %s TOTAL JOBS", len(all_secrets), len(all_jobs))
    for secret in sorted(all_secrets, key=lambda i: (len(i.url), i.url)):
        info("      Url: %s, Type: %s, Secret: %s", secret.url, secret.secret_type, secret.secret)


def log_related_issues_comments(all_issues, all_comments, all_projects):
    info("  FOUND %s ISSUES AND %s COMMENTS ACROSS %s PROJECTS", len(all_issues), len(all_comments), len(all_projects))


def log_related_snippets(all_snippets, all_projects):
    info("  FOUND %s SNIPPETS ACROSS %s TOTAL PROJECTS", len(all_snippets), len(all_projects))


def log_related_jobs(all_job_logs, all_projects):
    info("  FOUND %s JOB LOGS ACROSS %s TOTAL PROJECTS", len(all_job_logs), len(all_projects))


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
