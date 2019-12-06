# Token-Hunter

Collect OSINT for GitLab groups and members and search the group and group members' snippets, issues, and issue comments for sensitive data that may be included in these assets. The information gathered is intended to compliment and inform the use of additional tools such as [TruffleHog](https://github.com/dxa4481/truffleHog) or [GitRob](https://github.com/michenriksen/gitrob), which search git commit history using the regular expression matching.  Token-Hunter uses the same set of regular expressions as TruffleHog with a few additions for GitLab specific tokens.

# How the tool works

Start by providing a starting point such as a group ID on GitLab.  Token-Hunter will use the starting GitLab group to find all associated projects for that group.  Configure the tool to look for secrets in assets related to the group.  Currently, the tool supports GitLab Snippets, Issues, and Discussions/Comments with plans for future expansion to other assets.  The tool is intended to be very configurable to allow for efficient discovery of sensitive data. 

# Usage

Before running the tool, you will need to generate a GitLab API key and export it as an environment variable. This can be done as shown below:

```
export GITLAB_API_TOKEN=xxxxx
```

Next, install dependencies with:

```
pip3 install -r ./requirements.txt
```

Then, you can run the tool as follows:

```
usage: token-hunter.py [-h] -g GROUP [-u URL] [-m] [-s] [-i] [-t] [-p PROXY]
                    [-c CERT] [-l LOGFILE]

Collect OSINT for GitLab groups and members. Optionally search the group and
group members snippets, project issues, and issue discussions/comments for
sensitive data.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Optional argument that specifies the root url of your
                        GitLab instance. If the argument is not supplied, it
                        defaults to 'https://gitlab.com'
  -m, --members         Include group members personal projects and their
                        related assets in the searchfor sensitive data.
  -s, --snippets        Searches found projects for GitLab Snippets with
                        sensitive data.
  -i, --issues          Searches found projects for GitLab Issues and
                        discussions/comments with sensitive data.
  -t, --timestamp       Disables display of start/finish times and originating
                        IP to the output
  -p PROXY, --proxy PROXY
                        Proxies all requests using the provided URI matching
                        the scheme: http(s)://user:pass@10.10.10.10:8000
  -c CERT, --cert CERT  Used in tandem with -p (--proxy), this switch provides
                        a fully qualified path to a certificate to verify TLS
                        connections. Provide a fully qualified path to the
                        dynamic cert. Example:
                        /Users/<username>/owasp_zap_root_ca.cer.
  -l LOGFILE, --logfile LOGFILE
                        Will APPEND all output to specified file.

required arguments:
  -g GROUP, --group GROUP
                        ID or HTML encoded name of a GitLab group. This
                        option, by itself, will display group projects and
                        member names only.
```

Example: `./token-hunter.py -gmsi <123456>`

Runs token-hunter for group with ID 123456\. You can find the group ID for any group just underneath its name when viewing a group in the UI. The `-m` switch tells token-hunter to also dump information on any personal projects maintained by the members of that group. The `-s` switch tells token-hunter to search the [snippets](https://docs.gitlab.com/ee/user/snippets.html) maintained by the group and, since `-m` was provided, the groups members. The `-i` switch also tells token-hunter to search the [issues](https://docs.gitlab.com/ee/user/project/issues/) entered by the group and, since `-m` was provided, the issues on any of the group members personal projects for sensitive data.

# Project Status

Currently, only the following functions are implemented:

- GitLab group
- GitLab snippets search for secrets

The following will be added:

- GitLab project

The following are possible future improvements:

- Cross-referencing between GitHub and GitLab
- Additional social media sites like StackOverflow, Twitter, etc
