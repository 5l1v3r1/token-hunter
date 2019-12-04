# Git_OSINT

Collect OSINT for GitLab groups and members. You can optionally search the group and
group members snippets, issues, and issue comments for sensitive data that may be included in these assets. 
The information gathered is intended to compliment and inform the use of additional tools such as 
[TruffleHog](https://github.com/dxa4481/truffleHog) or [GitRob](https://github.com/michenriksen/gitrob), which search
git history in the same way.

# How it Works

You provide a starting point, like a group ID on GitLab. Git_OSINT will use the appropriate API to find all projects, 
users and snippets associated with that starting point, and enumerate git projects and they own or contribute to and 
will list all the snippets associated with each project in the group. In addition, if you provide the `-s` switch, all
[GitLab Snippets](https://docs.gitlab.com/ee/user/snippets.html) associated with each project in the group will be 
searched for sensitive information using the [set of regular expressions provided](./regexes.json). The starting set 
originated from open source project [TruffleHogRegex](https://github.com/dxa4481/truffleHogRegexes) and was 
appended to look for GitLab personal access tokens (PATs). You may alter this list as you see fit.

All data is printed to the console, and is optionally logged to a file.

# Usage

Before running the tool, you will need to generate a GitLab API key and export them 
it as an environment variable. This can be done as shown below:

``` 
export GITLAB_API_TOKEN=xxxxx
```

Next, install dependencies with:

``` 
pip3 install -r ./requirements.txt
```

Then, you can run the tool as follows:

``` 
usage: git_osint.py [-h] -g GROUP [-u URL] [-m] [-s] [-i] [-t] [-p PROXY]
                    [-c CERT] [-l LOGFILE]

Collect OSINT for GitLab groups and members. Optionally search the group and
group members snippets, issues, and issue comments for sensitive data.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Optional argument that specifies the root url for
                        scanning. If the argument is not supplied, it defaults
                        to 'https://gitlab.com'
  -m, --members         Includes group members personal projects, snippets,
                        issues, and issue comments in the search for secrets
  -s, --snippets        Searches the snippets associated with projects the
                        group maintains for secrets
  -i, --issues          Searches the issues and related comments associated
                        with the group for secrets
  -t, --timestamp       Disables display of start/finish times and originating
                        IP to the output
  -p PROXY, --proxy PROXY
                        Proxies all HTTP and TLS requests using the provided
                        URL matching the scheme:
                        http(s)://user:pass@10.10.10.10:8000
  -c CERT, --cert CERT  Used in tandem with -p (--proxy), this switch provides
                        a fully qualified path to a certificate to verify TLS
                        connections. Provide a fully qualified path to the
                        dynamic cert. Example:
                        /Users/<username>/owasp_zap_root_ca.cer.
  -l LOGFILE, --logfile LOGFILE
                        Will APPEND found items to specified file.

required arguments:
  -g GROUP, --group GROUP
                        ID or HTML encoded name of a GitLab group. This
                        option, by itself, will display group projects and
                        member names only.
```

Example:  `./git_osint.py -gmsi <123456>`

Runs Git_OSINT for group with ID 123456.  You can find the group ID for any group just underneath its name when viewing
a group in the UI.  The `-m` switch tells Git_OSINT to also dump information on any personal projects maintained by the
 members of that group.  The `-s` switch tells Git_OSINT to search the 
[snippets](https://docs.gitlab.com/ee/user/snippets.html) maintained by the group and, since `-m` was provided, 
the groups members.  The `-i` switch also tells Git_OSINT to search the 
[issues](https://docs.gitlab.com/ee/user/project/issues/) entered by the group and, since `-m` was
provided, the issues on any of the group members personal projects for sensitive data.

# Project Status

Currently, only the following functions are implemented:

* GitLab group
* GitLab snippets search for secrets

The following will be added:

* GitLab project

The following are possible future improvements:

* Cross-referencing between GitHub and GitLab
* Additional social media sites like StackOverflow, Twitter, etc