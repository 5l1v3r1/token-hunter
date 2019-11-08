import json
import os
import re
import argparse
import sys


class Arguments:

    class __Arguments:
        def __init__(self):
            parser = argparse.ArgumentParser(
                description="Collect OSINT for GitLab groups and members.  Optionally search the "
                            "group and group members snippets, issues, and issue comments for "
                            "sensitive data.")
            required_named = parser.add_argument_group('required arguments')
            required_named.add_argument('-g', '--group', type=str, action='append', required=True,
                                        help="ID or URL encoded name of a GitLab group.  This option, by itself, "
                                             "will display group projects and member names only.")
            parser.add_argument('-m', '--members', action='store_true',
                                help="Includes group members personal projects, snippets, issues, and issue comments "
                                     "in the search for secrets")
            parser.add_argument('-s', '--snippets', action='store_true',
                                help='Searches the snippets associated with projects the group maintains for secrets')
            parser.add_argument('-i', '--issues', action='store_true',
                                help="Searches the issues and related comments associated with the group for secrets")
            parser.add_argument('-t', '--timestamp', action='store_true',
                                help='Disables display of start/finish times and originating IP to the output')
            parser.add_argument('-p', '--proxy', type=str, action='store',
                                help='Proxies all HTTP and TLS requests using the provided URL matching the scheme:  '
                                     'http(s)://user:pass@10.10.10.10:8000')
            parser.add_argument('-v', '--verify-tls', type=str, action='store',
                                help='Used in tandem with -p, this switch provides a method to verify TLS connections '
                                     'using a dynamic cert. Provide a fully qualified path to the dynamic cert.  '
                                     'Example:  /Users/username/owasp_zap_root_ca.cer.')
            parser.add_argument('-l', '--logfile', type=str, action='store',
                                help='Will APPEND found items to specified file.')

            if len(sys.argv) == 1:
                parser.print_help(sys.stderr)
                sys.exit(1)

            self.parsed_args = parser.parse_args()
            if self.parsed_args.proxy and not self.parsed_args.verify_tls:
                parser.error('If you specify a proxy address, you must also specify a dynamic certificate in order to '
                             'decrypt TLS traffic with the --verify-tls switch.')

    instance = None

    def __init__(self):
        if not Arguments.instance:
            Arguments.instance = Arguments.__Arguments()

    def __getattr__(self, name):
        return getattr(self.instance.parsed_args, name)


class Issue:
    def __init__(self, ident, web_url, description):
        self.ident = ident
        self.web_url = web_url
        self.description = description


class Comment:
    def __init__(self, comment_type, parent_url, comment_body):
        self.comment_type = comment_type
        self.comment_body = comment_body
        self.parent_url = parent_url


class Secret:
    def __init__(self, secret_type, secret, url):
        self.secret_type = secret_type
        self.url = url
        self.secret = secret


class SecretsMonitor:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "../regexes.json"), 'r') as f:
            self.regexes = json.loads(f.read())
        for key in self.regexes:
            self.regexes[key] = re.compile(self.regexes[key])

    def sniff_secrets(self, content):
        if len(content.keys()) == 0:
            return []
        secrets = []
        for web_url, raw_data in content.items():
            found_secrets = self.__get_secrets(raw_data)
            for secret_type, secret in found_secrets.items():
                secrets.append(Secret(secret_type, secret, web_url))
        return secrets

    def __get_secrets(self, content):
        result = {}
        if not content:
            return result
        for key in self.regexes:
            match = self.regexes[key].search(content)
            if match:
                result.update({key: match.group()})
        return result
