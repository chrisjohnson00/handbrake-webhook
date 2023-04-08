from utilities.skip import should_skip


def test_should_skip():
    file = "/tv/The Daily Show/The Daily Show - 2023-04-06 - Jerry Craft WEBDL-1080p.mkv"
    skip_config = {'patterns_to_skip': [{'name': 'foobar', 'match_string': 'foobar'},
                                        {'name': 'foobar1', 'match_string': 'WEBDL'}]}
    assert should_skip(file_path=file, skip_config=skip_config)


def test_should_not_skip():
    file = "/tv/The Daily Show/The Daily Show - 2023-04-06 - Jerry Craft WEBDL-1080p.mkv"
    skip_config = {'patterns_to_skip': [{'name': 'foobar', 'match_string': 'foobar'},
                                        {'name': 'foobar1', 'match_string': 'foobar'}]}
    assert not should_skip(file_path=file, skip_config=skip_config)
