import textwrap
from osint_tools import gitlab_snippets_monitor


def test_handles_empty_string():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = ""
    assert target.get_secrets(content) == {}


def test_handles_nil():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = None
    assert target.get_secrets(content) == {}


def test_finds_simple_json_gitlab_pat():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = "API_KEY:a8pt01843901sdf0-a_1"
    assert target.get_secrets(content) == {"GitLab PAT": ":a8pt01843901sdf0-a_1"}


def test_regexes_are_loaded():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    assert len(target.regexes) > 0
    assert target.regexes["GitLab PAT"] is not None


def test_finds_gitlab_pat_in_text_block():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = textwrap.dedent("""\
            using System.Collections.Generic;
            using System.Runtime.CompilerServices;
            
            namespace NameSpace1
            {
                public static class DoubleExecutionPreventerExtensions
                {
                    private static readonly List<string> locks = new List<string>();
            
                    public static void Free(this object obj, [CallerMemberName] string caller = null)
                    {
                        string key = GetKey(obj, caller);
                        locks.Remove(key);
                    }
            
                    public static bool Lock(this object obj, [CallerMemberName] string caller = null)
                    {
                        string key = GetKey(obj, caller);
            
                        if (locks.Contains(key))
                            return true;
            
                        locks.Add(key);
                        return false;
                    }
            
                    private static string GetKey(object instance, string caller)
                    {
                        return "-1a890cm-kforemg980="
                    }
                }
            }
        """)
    assert target.get_secrets(content) == {"GitLab PAT": '"-1a890cm-kforemg980='}


def test_finds_naked_slack_token():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = "xoxp-912111665212-112233445566-112233445566-111111111111111111111111111111a1"
    assert target.get_secrets(content) == {"Slack Token": content}


def test_finds_ambiguous_tokens_in_text_block():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = textwrap.dedent("""\
        import enum
        import os
        
        from aircademy.fields import *
        from aircademy.filterutils import *
        from aircademy.record import BaseRecord
        
        
        class GoTCharacterRecord(BaseRecord):
            class Meta:
                token: "xoxp-912111665212-112233445566-112233445566-111111111111111111111111111111a1"
        
            # Some other stuff goes here
        
        
        # The fun part goes here
    """)
    assert target.get_secrets(content) == {
        "Slack Token": "xoxp-912111665212-112233445566-112233445566-111111111111111111111111111111a1",
        "GitLab PAT": '"xoxp-912111665212-11'
    }


def test_finds_single_group_results():
    target = gitlab_snippets_monitor.GitLabSnippetMonitor()
    content = textwrap.dedent("""\
            -----BEGIN RSA PRIVATE KEY-----
            asdfjwpoidnsohfohoiahsdfkjaksfdkasdfsdkfjlhkjhslkdjhdfjh
            -----END RSA PRIVATE KEY-----"
        """)
    assert target.get_secrets(content) == {
        "RSA private key": "-----BEGIN RSA PRIVATE KEY-----"
    }
