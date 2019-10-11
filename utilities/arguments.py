import argparse
import sys

from osint_tools import gitlab_checks


def parse():
    desc = "Collect OSINT from GitLab"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-g', '--group', type=str, action='append',
                        help='Name of a GitLab group')
    parser.add_argument('-s', '--snippets', type=str, action='append',
                        help='Enable search for snippets in gitlab for secrets.  ')
    parser.add_argument('-l', '--logfile', type=str, action='store',
                        help='Will APPEND found items to specified file.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def apply_all(args):
    if args.group:
        gitlab_checks.process_groups(args.group)
