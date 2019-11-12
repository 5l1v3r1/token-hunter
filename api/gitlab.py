from logging import warning

import os
import re
import requests
from logging import error
from utilities import types, constants
from retry import retry


args = types.Arguments()
base_url = constants.Urls.gitlab_com_base_url()


def get_issue_comments(project_id, issue_id):
    return get('{}/projects/{}/issues/{}/discussions'.format(base_url, project_id, issue_id))


def get_issues(project_id):
    return get('{}/projects/{}/issues'.format(base_url, project_id))


def get_project_snippets(project):
    return get('{}/projects/{}/snippets'.format(base_url, project))


def get_snippet_raw(snippet_id):
    return get('{}/snippets/{}/raw?line_ending=raw'.format(base_url, snippet_id))


def get_personal_projects(member):
    return get('{}/users/{}/projects'.format(base_url, member))


def get_group_projects(group):
    return get('{}/groups/{}/projects'.format(base_url, group))


def get_group(group):
    return get('{}/groups/{}'.format(base_url, group))


def get_members(group):
    return get('{}/groups/{}/members'.format(base_url, group))


def get_current_user():
    details = get('{}/user'.format(base_url))

    if not details:
        return False

    username = details['username']
    return username


def __get_verify_setting():
    if not args.verify_tls:
        return True
    return args.verify_tls


def __get_proxies():
    proxy_url = args.proxy
    if not proxy_url:
        return {}
    return {
        "http": proxy_url,
        "https": proxy_url,
    }


@retry(requests.exceptions.ConnectionError, delay=1, backoff=2, tries=10)
def __get(url):
    headers = {
        "PRIVATE-TOKEN": os.getenv(constants.Environment.gitlab_api_token()),
        "USER-AGENT": "git_osint"
    }
    response = requests.get(url, headers=headers, proxies=__get_proxies(), verify=__get_verify_setting())
    # if its not a timeout, log rate limiting info.  otherwise, these headers don't exist
    if response.status_code is not 504:
        log_rate_limit_info(response.headers["RateLimit-Observed"],
                            response.headers["RateLimit-Limit"],
                            response.headers["RateLimit-ResetTime"])
    return response


def get(url):
    """
    Helper function to interact with GitLab API using python requests

    The important things here are:
        - Adding the PRIVATE-TOKEN header based on env variable
        - interacting with the pagination process via LINK headers
          (https://docs.gitlab.com/ee/api/README.html#pagination)
    """

    response = __get(url)

    if response.status_code == 200:
        # The "Link" header is returned when there is more than one page of
        # results. GitLab asks that we use this link instead of crafting
        # our own.
        if 'Link' in response.headers.keys():
            # initialize a new variable to begin compounding multi-page
            # results
            all_results = response.json()
            # Now, loop through until there is no 'next' link provided
            pagenum = 2
            while 'Link' in response.headers.keys() and 'rel="next"' in response.headers['Link']:
                # Using print instead of logging, we don't want the per-page
                # status update in the log file

                regex = re.compile(r'<([^<>]*?)>; rel="next"')
                next_url = re.findall(regex, response.headers['Link'])[0]

                # Add the individual response to the collective
                response = __get(next_url)
                if response.status_code == 200:
                    all_results += response.json()
                else:
                    warning("[!] Error processing pagination URL: %s", next_url)
                pagenum += 1

            # Return the collective results
            return all_results

        # Otherwise, return just the single result
        if response.headers["Content-Type"] == "application/json":
            return response.json()
        return response.text

    # If code not 200, no results to process
    warning("[!] API failure. Details:")
    warning("    URL: %s", url)
    warning("    Response Code: %s Reason: %s", response.status_code, response.reason)
    return False


def log_rate_limit_info(observed, limit, reset_time):
    if int(observed) >= int(limit) - 10:
        error(f"[!] Nearing rate limit ({observed}/{limit})!  Reset time: {reset_time}.")
