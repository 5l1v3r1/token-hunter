from api import gitlab


def all_group_projects(group):
    return gitlab.get_group_projects(group)


def all_member_projects(member):
    return gitlab.get_personal_projects(member)
