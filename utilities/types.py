from collections import namedtuple
import argparse
import json
import os
import re
import sys

from utilities import constants


class Arguments:
    class __Arguments:
        def __init__(self):
            parser = argparse.ArgumentParser(
                description="Collect OSINT for GitLab groups and members.  Optionally search the "
                            "group and group members snippets, project issues, and issue discussions/comments for "
                            "sensitive data.")
            required_named = parser.add_argument_group('required arguments')
            required_named.add_argument('-g', '--group', type=str, action='append', required=True,
                                        help="ID or HTML encoded name of a GitLab group.  This option, by itself, "
                                             "will display group projects and member names only.")
            parser.add_argument('-u', '--url', default='https://gitlab.com',
                                help="An optional argument to specify the base URL of your GitLab instance.  If the "
                                     "argument is not supplied, its defaulted to 'https://gitlab.com'")
            parser.add_argument('-m', '--members', action='store_true',
                                help="Include group members personal projects and their related assets in the search"
                                     "for sensitive data.")
            parser.add_argument('-s', '--snippets', action='store_true',
                                help="Searches found projects for GitLab Snippets with sensitive data.")
            parser.add_argument('-i', '--issues', action='store_true',
                                help="Searches found projects for GitLab Issues and discussions/comments with sensitive "
                                     "data.")
            parser.add_argument('-r', '--mergerequests', action='store_true',
                                help="Searches found projects for GitLab Merge Requests and discussions/comments with "
                                     "sensitive data.")
            parser.add_argument('-t', '--timestamp', action='store_true',
                                help='Disables display of start/finish times and originating IP to the output')
            parser.add_argument('-p', '--proxy', type=str, action='store',
                                help='Proxies all requests using the provided URI matching the scheme:  '
                                     'http(s)://user:pass@10.10.10.10:8000')
            parser.add_argument('-c', '--cert', type=str, action='store',
                                help='Used in tandem with -p (--proxy), this switch provides a fully qualified path to a '
                                     'certificate to verify TLS connections. Provide a fully qualified path to the dynamic '
                                     'cert. Example:  /Users/<username>/owasp_zap_root_ca.cer.')
            parser.add_argument('-l', '--logfile', type=str, action='store',
                                help='Will APPEND all output to specified file.')

            constants.Banner.render()

            if len(sys.argv) == 1:
                parser.print_help(sys.stderr)
                sys.exit(1)

            self.parsed_args = parser.parse_args()
            if self.parsed_args.proxy and not self.parsed_args.cert:
                parser.error('If you specify a proxy address, you must also specify a dynamic certificate in order to '
                             'decrypt TLS traffic with the --verify-tls switch.')

    instance = None

    def __init__(self):
        if not Arguments.instance:
            Arguments.instance = Arguments.__Arguments()

    def __getattr__(self, name):
        return getattr(self.instance.parsed_args, name)


Issue = namedtuple('Issue', 'ident web_url description')
Comment = namedtuple('Comment', 'comment_type parent_url comment_body')
Secret = namedtuple('Secret', 'secret_type secret url')


class SecretsMonitor:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "../regexes.json")) as f:
            self.regexes = json.loads(f.read())

        self.regex_names = self.__regex_names(self.regexes)
        self.master_regex = self.__compile_regexes(self.regexes)

    def __regex_names(self, regexes):
        """ Returns a dict containing regex names keyed by group
        """
        return {self.__group(i): name for i, name in enumerate(regexes)}

    def __compile_regexes(self, regexes):
        """ Concatenates all regexes into one big, compiled regex.
        """
        parts = []
        for i, name in enumerate(regexes):
            group = self.__group(i)
            regex = regexes[name]
            parts.append(f'(?P<{group}>{regex})')

        return re.compile('|'.join(parts), re.IGNORECASE)

    def __group(self, i):
        return f'group_{i}'

    def sniff_secrets(self, content):
        if not content:
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
        match = self.master_regex.search(content)
        if not match:
            return result
        for group, value in match.groupdict().items():
            if value is None:
                continue
            name = self.regex_names[group]
            result[name] = value
        return result
