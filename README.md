# Git_OSINT

Git_OSINT can be used to gather intelligence from groups and projects hosted on GitLab and GitHub. The information gathered may be useful to feed into additional tools such as [TruffleHog](https://github.com/dxa4481/truffleHog) or [GitRob](https://github.com/michenriksen/gitrob).

The idea is that a contributor may commit sensitive data to their own personal projects, which are not watched as closely as the primary shared projects they are working on.

# How it Works
You provide a starting point, like a group name on GitLab. This tool will use the appropriate API to find all users associated with that starting point, and enumerate git projects they own or contribute to.

All data is printed to the console, and is optionally logged to a file.

# Usage
Before running the tool, you will need to generate an API key for the site/s your wish to interact with and export them as environment variables. This can be done as shown below:

```
export GITLAB_API=xxxxx
export GITHUB_API=xxxxx
```

If you are only querying GitLab, you only need to set that key. The same applies for GitHub.

Then, you can run the tool as follows:

```
usage: git_osint.py [-h] [-g GROUP] [-p PROJECT] [-t TEAM] [-r REPO]
                    [-l LOGFILE]

Collect OSINT from GitLab and GitHub

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP, --group GROUP
                        Name of a GitLab group
  -p PROJECT, --project PROJECT
                        Name of a GitLab project
  -t TEAM, --team TEAM  Name of a GitHub team
  -r REPO, --repo REPO  Name of a GitHub repo
  -l LOGFILE, --logfile LOGFILE
                        Will APPEND found items to specified file.
```

# Project Status
Currently, only the following functions are implemented:
- GitLab group

The following will be added:
- GitLab project
- GitHub team
- GitHub repo

The following are possible future improvements:
- Cross-referencing between GitHub and GitLab
- Additional social media sites like StackOverflow, Twitter, etc
