# Git_OSINT

Git_OSINT can be used to gather intelligence from groups and projects hosted on GitLab. The information gathered may be 
useful to feed into additional tools such as [TruffleHog](https://github.com/dxa4481/truffleHog) 
or [GitRob](https://github.com/michenriksen/gitrob).

The idea is that a contributor may commit sensitive data to their own personal projects, which are not watched as 
closely as the primary shared projects they are working on.

Currently, secrets detection is performed for GitLab snippets only by adding the `-s` switch documented below.

# How it Works
You provide a starting point, like a group ID on GitLab. This tool will use the appropriate API to find all projects, 
users and snippets associated with that starting point, and enumerate git projects and they own or contribute to and 
will list all the snippets associated with each project in the group.  In addition, if you provide the `-s` switch, all
[GitLab Snippets](https://docs.gitlab.com/ee/user/snippets.html) associated with each project in the group will be 
searched for sensitive information using the [set of regular expressions provided](./regexes.json).  The starting set 
originated from open source project [TruffleHogRegex](https://github.com/dxa4481/truffleHogRegexes) and was 
appended to look for GitLab personal access tokens (PATs).  You may alter this list as you see fit.

All data is printed to the console, and is optionally logged to a file.

# Usage
Before running the tool, you will need to generate a GitLab API key and export them 
it as an environment variable. This can be done as shown below:

```
export GITLAB_API=xxxxx
```

Next, install dependencies with:
```
pip3 install -r ./requirements.txt
```

Then, you can run the tool as follows:

```
Collect OSINT for GitLab Groups, Projects, Members, and Snippets

optional arguments:
  -h, --help            show this help message and exit
  -s, --snippets        Searches the snippets associated with projects the
                        group maintains for secrets
  -l LOGFILE, --logfile LOGFILE
                        Will APPEND found items to specified file.

required arguments:
  -g GROUP, --group GROUP
                        ID or name of a GitLab group
```

Examples:
`./git_osint.py -g <123456>`
Runs Git OSINT for the group specified, dumping the URLs for each project maintained by the group as well as all project
URLs for the members in that group.

`./git_osint.py -g <123456> -s`
Same as above with one functional addition.  The `-s` switch will tell the application to search for all 
[GitLab Snippets](https://docs.gitlab.com/ee/user/snippets.html) associated with each project the group maintains, as
well as snippets for each personal project maintained by members of the group.

# Project Status
Currently, only the following functions are implemented:
- GitLab group
- GitLab snippets search for secrets

The following will be added:
- GitLab project

The following are possible future improvements:
- Cross-referencing between GitHub and GitLab
- Additional social media sites like StackOverflow, Twitter, etc
- Searching for secrets within GitLab repository historical commits.
