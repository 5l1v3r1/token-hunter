import requests
import requests_mock
import pytest

from api import gitlab


def test_gitlab_basic_get(requests_mock):
    expected_url = "http://gitlab.com/api/v4/user"
    expected_json = {"username": "codeEmitter"}
    requests_mock.register_uri("GET", expected_url, json=expected_json, status_code=200, headers={
        "RateLimit-Observed": "500",
        "RateLimit-Limit": "600",
        "RateLimit-ResetTime": "1/1/2020",
        "Content-Type": "application/json"}
    )
    target = gitlab.GitLab(lambda: requests.Session())
    assert target.get(expected_url) == expected_json
    assert requests_mock.called is True
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == "GET"
    assert requests_mock.request_history[0].url == expected_url


def test_gitlab_pages_requests_properly(requests_mock):
    expected_url_initial = "http://gitlab.com/api/v4/groups/1"
    expected_url_paged = "https://gitlab.com/api/v4/groups/1/members?id=1&page=2&per_page=20"
    request1_json = {"username": "codeEmitter"}
    request2_json = {"username": "jsmith"}
    url1_headers = {
        "RateLimit-Observed": "500",
        "RateLimit-Limit": "600",
        "RateLimit-ResetTime": "1/1/2020",
        "Content-Type": "application/json",
        "Link": f'<{expected_url_paged}>; rel="next", <https://gitlab.com/api/v4/groups/1/members?id=1&page=1&per_page=20>; rel="first", <https://gitlab.com/api/v4/groups/1/members?id=1&page=2&per_page=20>; rel="last"'
    }
    url2_headers = {
        "RateLimit-Observed": "500",
        "RateLimit-Limit": "600",
        "RateLimit-ResetTime": "1/1/2020",
        "Content-Type": "application/json",
        "Link": '<https://gitlab.com/api/v4/groups/3786502/members?id=3786502&page=1&per_page=20>; rel="prev", <https://gitlab.com/api/v4/groups/3786502/members?id=3786502&page=1&per_page=20>; rel="first", <https://gitlab.com/api/v4/groups/3786502/members?id=3786502&page=2&per_page=20>; rel="last"'
    }

    requests_mock.register_uri("GET", expected_url_initial, json=[request1_json], status_code=200, headers=url1_headers)
    requests_mock.register_uri("GET", expected_url_paged, json=[request2_json], status_code=200, headers=url2_headers)
    target = gitlab.GitLab(lambda: requests.Session())
    assert target.get(expected_url_initial) == [request1_json, request2_json]
    assert requests_mock.called is True
    assert requests_mock.call_count == 2
    assert requests_mock.request_history[0].method == "GET"
    assert requests_mock.request_history[0].url == expected_url_initial
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == expected_url_paged


def test_gitlab_handles_a_unpaged_timeout_correctly(requests_mock):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        expected_url = "http://gitlab.com/api/v4/members/1"
        requests_mock.register_uri("GET", expected_url, exc=requests.exceptions.ConnectTimeout)
        target = gitlab.GitLab(lambda: requests.Session())
        target.get(expected_url)


