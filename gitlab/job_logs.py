from utilities import types, validate
from api import gitlab
from logging import info

gitlab = gitlab.GitLab(types.Arguments().url)


def get_all(project_id, project_url):
    job_logs = []
    jobs = gitlab.get_jobs(project_id)
    if validate.api_result(jobs):
        info("[*] Found %s jobs for project %s", len(jobs), project_url)
        for job in jobs:
            job_log = gitlab.get_job_logs(project_id, job['id'])
            job_logs.append(types.JobLog(job['id'], job['web_url'], job_log))
    return job_logs


def sniff_secrets(job_log):
    monitor = types.SecretsMonitor()
    return monitor.sniff_secrets({job_log.web_url: job_log.trace})

