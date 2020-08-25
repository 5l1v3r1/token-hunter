from utilities import constants


def truncate(target):
    return (target[:constants.Strings.max_string_length()] + "...") \
        if len(target) > constants.Strings.max_string_length() \
        else target
