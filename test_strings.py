from utilities import strings


def test_truncate_does_not_change_short_string():
    target = "This is a test."
    result = strings.truncate(target)
    assert result == target


def test_truncate_changes_long_single_line_string():
    target = "When words become unclear, I shall focus with photographs. When images become inadequate, I shall be content with silence."
    result = strings.truncate(target)
    assert result == "When words become unclear, I shall focus with photographs. When images beco..."


def test_truncate_changes_long_string_with_carriage_return():
    target = "[0KRunning with gitlab-runner 12.10.0-rc2 (6c8c540f) " \
             "[0;m[0K  on docker-auto-scale-com 8a6210b8" \
             "[0;msection_start:1588924722:prepare_executor" \
             "[0K[0K[36;1mPreparing the \"docker+machine\" executor[0;m"
    result = strings.truncate(target)
    assert result == "[0KRunning with gitlab-runner 12.10.0-rc2 (6c8c540f) " \
                     "[0;m[0K  on docker-au..."


