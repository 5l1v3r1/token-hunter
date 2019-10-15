from osint_tools import gitlab_snippets


def test_handles_empty_string():
    content = ""
    result = gitlab_snippets.get_secrets(content)
    assert result == []
