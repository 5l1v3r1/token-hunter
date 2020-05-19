import textwrap
from utilities import types

test_url = "https://www.test.com/api/v1/test"


def test_handles_empty_string():
    target = types.SecretsMonitor()
    content = {test_url: ""}
    assert target.sniff_secrets(content) == []


def test_handles_nil():
    target = types.SecretsMonitor()
    content = {test_url: None}
    assert target.sniff_secrets(content) == []


def test_finds_simple_json_gitlab_pat():
    target = types.SecretsMonitor()

    content = {test_url: "private-token:AB123mr980pas453201s"}
    actual = target.sniff_secrets(content)
    assert len(actual) == 1
    assert actual[0].url == test_url
    assert actual[0].secret == "-token:AB123mr980pas453201s"
    assert actual[0].secret_type == "GitLab PAT"


def test_regexes_are_loaded():
    target = types.SecretsMonitor()
    assert len(target.regexes) > 0


def test_does_not_match_gitlab_pats_without_line_ending():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""
        [GitLab Personal Access Token Example](https://gitlab.com/gitlab-com/gl-security/gl-redteam/red-team-tech-notes/snippets/1976052)
    """)}
    actual = target.sniff_secrets(content)
    assert len(actual) == 0


def test_finds_gitlab_pat_in_text_block():
    target = types.SecretsMonitor()
    content = {test_url: "return gitlabtoken=\"asdfkDjfkjalkSjdflkj\""}
    actual = target.sniff_secrets(content)
    assert len(actual) == 1
    assert actual[0].secret == 'token="asdfkDjfkjalkSjdflkj"'
    assert actual[0].url == test_url
    assert actual[0].secret_type == "GitLab PAT"


def test_finds_naked_slack_token():
    target = types.SecretsMonitor()
    naked_token = "xoxp-912111665212-112233445566-112233445566-111111111111111111111111111111a1"
    content = {test_url: naked_token}
    actual = target.sniff_secrets(content)
    assert len(actual) == 1
    assert actual[0].url == test_url
    assert actual[0].secret == naked_token
    assert actual[0].secret_type == "Slack Token"


def test_finds_single_group_results():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
            -----BEGIN RSA PRIVATE KEY-----
            asdfjwpoidnsohfoHoiahsdfkjaksfdkasdfsdkfjlhkjhslkdjhdfjh
            -----END RSA PRIVATE KEY-----
        """)}
    assert len(target.sniff_secrets(content)) == 1


def test_finds_openssh_private_key():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
                    -----BEGIN OPENSSH PRIVATE KEY-----
                    asdfjwpoidnsohfoHoiahsdfkjaksfdkasdfsdkfjlhkjhslkdjhdfjh
                    -----END OPENSSH PRIVATE KEY-----"
                """)}
    assert len(target.sniff_secrets(content)) == 1


def test_finds_gitlab_ci_registration_token():
    target = types.SecretsMonitor()
    content = {test_url: "token: guz_DJCzb4rsUybpwuAQ"}
    assert len(target.sniff_secrets(content)) == 1
