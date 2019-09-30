import argparse
import sys


def parse():
    desc = "Collect OSINT from GitLab and GitHub"
    parser = argparse.ArgumentParser(description=desc)

    # Any combination, including multiple of each, of projects,
    # groups, repos, snippets, and teams.
    parser.add_argument('-g', '--group', type=str, action='append',
                        help='Name of a GitLab group')
    parser.add_argument('-p', '--project', type=str, action='append',
                        help='Name of a GitLab project')
    parser.add_argument('-t', '--team', type=str, action='append',
                        help='Name of a GitHub team')
    parser.add_argument('-r', '--repo', type=str, action='append',
                        help='Name of a GitHub repo')
    parser.add_argument('-s', '--snippets', type=str, action='append',
                        help="Enable search for snippets in gitlab for secrets")
    parser.add_argument('-l', '--logfile', type=str, action='store',
                        help='Will APPEND found items to specified file.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()