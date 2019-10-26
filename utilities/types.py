import json
import os
import re
import logging
import sys


class Logger:
    def __init__(self, logfile):
        logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

        # Add a logging handler for a file, if the user provides one
        if logfile:
            logging.getLogger().addHandler(logging.FileHandler(logfile))


class Secret:
    def __init__(self, secret_type, secret, url):
        self.secret_type = secret_type
        self.url = url
        self.secret = secret


class GitLabSnippetMonitor:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "../regexes.json"), 'r') as f:
            self.regexes = json.loads(f.read())
        for key in self.regexes:
            self.regexes[key] = re.compile(self.regexes[key])

    def get_secrets(self, content):
        result = {}
        if not content:
            return result
        for key in self.regexes:
            match = self.regexes[key].search(content)
            if match:
                result.update({key: match.group()})
        return result
