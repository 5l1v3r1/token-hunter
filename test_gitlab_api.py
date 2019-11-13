import requests
import requests_mock

from api import gitlab


def test_gitlab_get():
    uri = "mock://gitlab.com/api/v4/user"
    expected_json = {'username': 'codeEmitter'}

    def session_builder():
        session = requests.Session()
        adapter = requests_mock.Adapter()
        adapter.register_uri("GET", uri, json=expected_json, status_code=200, headers={"RateLimit-Observed": "600", "RateLimit-Limit": "600", "RateLimit-ResetTime": "1/1/2020", "Content-Type": "application/json"})
        session.mount('mock', adapter)
        return session
    target = gitlab.GitLab(session_builder)
    response = target.get(uri)
    assert response == expected_json
