import requests
import requests_mock

# from api import gitlab


def __arrange(verb, uri, expected_result):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    adapter.register_uri(verb, uri, text=expected_result)
    session.mount('mock', adapter)
    return session


def test_gitlab_get():
    session = __arrange('GET', 'http://someurl.com/test', 'data')
    # response = gitlab.get("http://someurl.com", session)
