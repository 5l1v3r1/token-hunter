
def truncate(target):
    return (target[:75] + "...") if len(target) > 75 else target
