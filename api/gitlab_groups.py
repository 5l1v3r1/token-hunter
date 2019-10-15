from api import gitlab


def all_groups(group):
    return gitlab.get_group(group)


def all_members(group):
    return gitlab.get_members(group)


