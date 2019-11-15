from logging import warning

import os
import re
import requests
from logging import error
from utilities import types, constants
from retry import retry


def build_session():
    command_args = types.Arguments()

    def get_cert():
        if not command_args.cert:
            return True
        return command_args.cert

    def get_proxies():
        proxy_url = command_args.proxy
        if not proxy_url:
            return {}
        return {
            "http": proxy_url,
            "https": proxy_url,
        }

    session = requests.session()
    session.headers.update({
        "PRIVATE-TOKEN": os.getenv(constants.Environment.gitlab_api_token()),
        "USER-AGENT": "git_osint"
    })
    session.proxies = get_proxies()
    session.verify = get_cert()
    return session


class Http:

    def __init__(self, session_builder):
        self.session = session_builder()

    @retry(requests.exceptions.ConnectionError, delay=constants.Requests.retry_delay(),
           backoff=constants.Requests.retry_backoff(), tries=constants.Requests.retry_max_tries())
    def get(self, url):
        response = self.session.get(url)
        # if its not a timeout, log rate limiting info.  otherwise, these headers don't exist
        if response.status_code is not 504:
            self.log_rate_limit_info(response.headers["RateLimit-Observed"],
                                     response.headers["RateLimit-Limit"],
                                     response.headers["RateLimit-ResetTime"])
        return response

    @staticmethod
    def log_rate_limit_info(observed, limit, reset_time):
        if int(observed) >= int(limit) - 10:
            error(f"[!] Nearing rate limit ({observed}/{limit})!  Reset time: {reset_time}.")


class GitLab:

    def __init__(self, session_builder=build_session):
        self.http = Http(session_builder)
        self.base_url = constants.Urls.gitlab_com_base_url()

    def get_issue_comments(self, project_id, issue_id):
        return self.get('{}/projects/{}/issues/{}/discussions'.format(self.base_url, project_id, issue_id))

    def get_issues(self, project_id):
        return self.get('{}/projects/{}/issues'.format(self.base_url, project_id))

    def get_project_snippets(self, project):
        return self.get('{}/projects/{}/snippets'.format(self.base_url, project))

    def get_snippet_raw(self, snippet_id):
        return self.get('{}/snippets/{}/raw?line_ending=raw'.format(self.base_url, snippet_id))

    def get_personal_projects(self, member):
        return self.get('{}/users/{}/projects'.format(self.base_url, member))

    def get_group_projects(self, group):
        return self.get('{}/groups/{}/projects'.format(self.base_url, group))

    def get_group(self, group):
        return self.get('{}/groups/{}'.format(self.base_url, group))

    def get_members(self, group):
        return self.get('{}/groups/{}/members'.format(self.base_url, group))

    def get_current_user(self):
        details = self.get('{}/user'.format(self.base_url))

        if not details:
            return False

        username = details['username']
        return username

    def get(self, url):
        """
        Helper function to interact with GitLab API using python requests

        The important things here are:
            - Adding the PRIVATE-TOKEN header based on env variable
            - interacting with the pagination process via LINK headers
              (https://docs.gitlab.com/ee/api/README.html#pagination)
        """

        response = self.http.get(url)

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
                    response = self.http.get(next_url)
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
