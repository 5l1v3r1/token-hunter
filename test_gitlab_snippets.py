from osint_tools import gitlab_snippets_monitor


def test_handles_empty_string():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = ""
    assert target.get_secrets(content) == []


def test_handles_nil():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = None
    assert target.get_secrets(content) == []


def test_finds_gitlab_pat():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = "a8pt01843901sdf0-a_1"
    assert target.get_secrets(content) == [content]


def test_regexes_are_loaded():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    assert len(target.regexes) > 0
    assert target.regexes["GitLab PAT"] is not None

