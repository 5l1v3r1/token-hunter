import json
import os


class GitLabSnippetMonitor:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "../regexes.json"), 'r') as f:
            self.regexes = json.loads(f.read())

    def get_secrets(self, content):
        if not content:
            return []
        return [content]
