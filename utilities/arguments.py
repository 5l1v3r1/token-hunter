import argparse
import sys

from osint_tools import gitlab_checks


def parse():
    parser = argparse.ArgumentParser(description="Collect OSINT for GitLab Groups, Projects, Members, and Snippets")
    required_named = parser.add_argument_group('required arguments')
    required_named.add_argument('-g', '--group', type=str, action='append', required=True,
                                help='ID or name of a GitLab group.  This option, by itself, will display group '
                                     'projects and member names only.')
    parser.add_argument('-m', '--members', action='store_true',
                        help="Searches for group members' personal projects and includes them in searches designated "
                             "by other switches")
    parser.add_argument('-s', '--snippets', action='store_true',
                        help='Searches the snippets associated with projects the group maintains for secrets')
    parser.add_argument('-i', '--issues', action='store_true',
                        help='Searches the issues associated with the group for secrets')
    parser.add_argument('-t', '--timestamp', action='store_true',
                        help='Appends start/finish times and originating IP to the output')
    parser.add_argument('-l', '--logfile', type=str, action='store',
                        help='Will APPEND found items to specified file.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def apply_all(args):
    if args.group:
        gitlab_checks.process_all(args)
