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
    assert target.get_secrets(content) == {"GitLab PAT": "a8pt01843901sdf0-a_1"}


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
    assert target.get_secrets(content) == {"GitLab PAT": "-1a890cm-kforemg980="}
