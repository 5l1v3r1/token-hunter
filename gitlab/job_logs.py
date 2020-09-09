from utilities import types, validate
from api import gitlab
from logging import info, warning

gitlab = gitlab.GitLab(types.Arguments().url)
args = types.Arguments()


def get_all(project_id, project_url):
    job_logs = []
    jobs = gitlab.get_jobs(project_id)
    if validate.api_result(jobs):
        limit = args.depth
        warning("[*] Found %s jobs for project %s.  Limiting scan depth (--depth) to %s", len(jobs), project_url, limit)
        i = 0
        for job in jobs:
            info("[*] Retrieving job %s for %s which completed at %s", job['id'], project_url, job['finished_at'])
            job_log = gitlab.get_job_logs(project_id, job['id'])
            job_logs.append(types.JobLog(job['id'], job['web_url'], job_log))
            i += 1
            if i == limit:
                break
    return job_logs


def sniff_secrets(job_log):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({job_log.web_url: job_log.trace})

