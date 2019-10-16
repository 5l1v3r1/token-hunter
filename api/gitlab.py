import requests
import os
import re

from logging import warning, info

BASE_URL = 'https://gitlab.com/api/v4'


def get_project_snippets(project):
    return get('{}/projects/{}/snippets'.format(BASE_URL, project))


def get_snippet_raw(snippet_id):
    return get('{}/snippets/{}/raw?line_ending=raw'.format(BASE_URL, snippet_id))


def get_personal_projects(member):
    return get('{}/users/{}/projects'.format(BASE_URL, member))


def get_group_projects(group):
    return get('{}/groups/{}/projects'.format(BASE_URL, group))


def get_group(group):
    return get('{}/groups/{}'.format(BASE_URL, group))


def get_members(group):
    return get('{}/groups/{}/members'.format(BASE_URL, group))


def get_current_user():
    details = get('{}/user'.format(BASE_URL))

    if not details:
        return False

    username = details['username']
    return username


def get(url):
    """
    Helper function to interact with GitLab API using python requests

    The important things here are:
        - Adding the PRIVATE-TOKEN header based on env variable
        - interacting with the pagination process via LINK headers
          (https://docs.gitlab.com/ee/api/README.html#pagination)
    """

    headers = {'PRIVATE-TOKEN': os.getenv('GITLAB_API')}
    response = requests.get(url, headers=headers)

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
                response = requests.get(next_url, headers=headers)
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
