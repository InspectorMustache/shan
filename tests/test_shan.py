from shan import volumes


def test_volumes():
    str_volume_list = volumes.get_str_volume_list()
    print(str_volume_list)
    for str_ in str_volume_list:
        assert isinstance(str_, str)


def test_tui():
    """Test TU interface."""
    pass
