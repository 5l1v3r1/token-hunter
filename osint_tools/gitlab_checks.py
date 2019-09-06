"""
GitLab specific checks for GitOSINT
"""

def get_project_members(target):
    """
    Returns a list of all members in a project
    """
    return

def get_personal_projects(members):
    """
    Returns a list of all personal projects for a list of members
    """
    return

def process_project(target):
    """
    Process a GitLab project
    """
    return

def process_group(target):
    """
    Process a GitLab group
    """
    members = get_project_members(target)
    personal_projects = get_personal_projects(members)

