import requests
import requests_mock

from api import gitlab


def test_gitlab_basic_get():
    expected_url = "http://gitlab.com/api/v4/user"
    expected_json = {"username": "codeEmitter"}
    with requests_mock.mock() as m:
        m.register_uri("GET", expected_url, json=expected_json, status_code=200, headers={
            "RateLimit-Observed": "500",
            "RateLimit-Limit": "600",
            "RateLimit-ResetTime": "1/1/2020",
            "Content-Type": "application/json"})
        target = gitlab.GitLab(lambda: requests.Session())
        response = target.get(expected_url)
        assert response == expected_json
        assert m.called is True
        assert m.call_count == 1
        assert m.request_history[0].method == "GET"
        assert m.request_history[0].url == expected_url
