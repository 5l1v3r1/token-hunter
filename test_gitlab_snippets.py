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

    content = {test_url: "API_KEY:a8pt01843901sdf0-a_1"}
    actual = target.sniff_secrets(content)
    assert len(actual) == 1
    assert actual[0].url == test_url
    assert actual[0].secret == ":a8pt01843901sdf0-a_1"
    assert actual[0].secret_type == "GitLab PAT"


def test_regexes_are_loaded():
    target = types.SecretsMonitor()
    assert len(target.regexes) > 0
    assert target.regexes["GitLab PAT"] is not None


def test_finds_gitlab_pat_in_text_block():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
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
        """)}
    actual = target.sniff_secrets(content)
    assert len(actual) == 1
    assert actual[0].secret == '"-1a890cm-kforemg980='
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


def test_finds_ambiguous_tokens_in_text_block():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
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
    """)}
    actual = target.sniff_secrets(content)
    assert len(actual) == 2
    assert actual[0].secret_type == "GitLab PAT"
    assert actual[0].url == test_url
    assert actual[0].secret == '"xoxp-912111665212-11'
    assert actual[1].secret_type == "Slack Token"
    assert actual[1].url == test_url
    assert actual[1].secret == "xoxp-912111665212-112233445566-112233445566-111111111111111111111111111111a1"


def test_finds_single_group_results():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
            -----BEGIN RSA PRIVATE KEY-----
            asdfjwpoidnsohfohoiahsdfkjaksfdkasdfsdkfjlhkjhslkdjhdfjh
            -----END RSA PRIVATE KEY-----
        """)}
    assert len(target.sniff_secrets(content)) == 1


def test_finds_openssh_private_key():
    target = types.SecretsMonitor()
    content = {test_url: textwrap.dedent("""\
                    -----BEGIN OPENSSH PRIVATE KEY-----
                    asdfjwpoidnsohfohoiahsdfkjaksfdkasdfsdkfjlhkjhslkdjhdfjh
                    -----END OPENSSH PRIVATE KEY-----"
                """)}
    assert len(target.sniff_secrets(content)) == 1
